"""cycle1072: 10-genre cinematic light accents for the 0–2.9s hook.

Only render over an explicit SHA-256-approved source. Does not change speech,
subtitles, or any scene after the hook. Review-only; never publish or upload media.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS, NFRAMES = 1080, 1920, 30, 691
START, END = 0, 87
OVERLAY_Y, OVERLAY_H = 385, 780  # all pixels below the top hook and above subtitles
PALETTES = {
    'ai_work': (55, 227, 244), 'finance': (242, 195, 106),
    'education': (117, 168, 252), 'health': (120, 224, 172),
    'travel': (248, 169, 187), 'beauty': (213, 166, 251),
    'food': (255, 166, 115), 'career': (112, 206, 239),
    'productivity': (184, 226, 113), 'lifestyle': (246, 201, 126),
}

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''):h.update(c)
    return h.hexdigest()

def probe(path):
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(s for s in d['streams'] if s['codec_type']=='video')
    a=next(s for s in d['streams'] if s['codec_type']=='audio')
    return {'video':v['codec_name'],'width':v['width'],'height':v['height'],
            'fps':v['r_frame_rate'],'audio':a['codec_name'],'sample_rate':int(a['sample_rate']),
            'duration':float(d['format']['duration'])}

def frame_overlay(frame, genre='ai_work'):
    if genre not in PALETTES:raise ValueError('unsupported genre')
    if not START<=frame<END:raise ValueError('frame out of range')
    color=PALETTES[genre]
    # Only the robot/ambient portion of scene 1, never captions, question or CTA.
    im=Image.new('RGBA',(W,OVERLAY_H),(0,0,0,0))
    halo=Image.new('RGBA',im.size,(0,0,0,0))
    d=ImageDraw.Draw(halo)
    phase=frame/FPS
    # Slow luminous bokeh drifting in the dark margins around the robot.
    for i,(cx,cy,rad) in enumerate(((110,265,20),(945,300,23),(130,555,16),(930,640,18),(830,95,13))):
        x=cx+16*math.sin(phase*1.5+i*1.4)
        y=cy+11*math.cos(phase*1.2+i*1.7)
        a=round(28+18*(0.5+0.5*math.sin(phase*2+i)))
        d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=(*color,a))
    halo=halo.filter(ImageFilter.GaussianBlur(24))
    im.alpha_composite(halo)
    # A traveling rim-light follows the left edge, then the right edge.
    lines=Image.new('RGBA',im.size,(0,0,0,0))
    dl=ImageDraw.Draw(lines)
    t=frame/(END-1)
    theta=-1.6+3.5*t
    x=540+416*math.cos(theta)
    y=420+340*math.sin(theta)
    # Glint is faint enough not to occlude the robot or alter the words.
    for r,a in ((24,10),(12,28),(5,90)):
        dl.ellipse((x-r,y-r,x+r,y+r),fill=(*color,a))
    # Short orbit accent: a visually changing cue rather than a fixed border.
    pts=[]
    for j in range(28):
        ang=theta-0.36+j*0.36/27
        pts.append((540+416*math.cos(ang),420+340*math.sin(ang)))
    dl.line(pts,fill=(*color,100),width=3,joint='curve')
    im.alpha_composite(lines)
    return im

def compose(source,out,expected_sha,genre='ai_work'):
    if genre not in PALETTES:raise ValueError('unsupported genre')
    if sha256(source)!=expected_sha:raise ValueError('source SHA256 mismatch; fail closed')
    p=probe(source)
    if (p['video'],p['width'],p['height'],p['fps'],p['audio'],p['sample_rate'])!=('h264',W,H,'30/1','aac',48000):
        raise ValueError('unexpected video/audio input')
    if abs(p['duration']-23.033333)>.08:raise ValueError('unexpected duration')
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        for i in range(START,END):frame_overlay(i,genre).save(root/f'{i:04d}.png',compress_level=1)
        Path(out).parent.mkdir(parents=True,exist_ok=True)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-start_number','0','-i',str(root/'%04d.png'),
             '-filter_complex',f'[1:v]format=rgba,setpts=PTS+{START}/{FPS}/TB[light];'
             f'[0:v][light]overlay=x=0:y={OVERLAY_Y}:eof_action=pass:shortest=0:format=auto[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(NFRAMES),
             '-c:a','copy','-movflags','+faststart',str(out)]
        subprocess.run(cmd,check=True)
    return probe(out)

def smoke():
    # 3 seconds only, never touch private media in CI.
    with tempfile.TemporaryDirectory() as td:
        p=Path(td);source=p/'src.mp4';out=p/'out.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
            '-f','lavfi','-i','color=c=#051729:s=1080x1920:r=30:d=23.033333',
            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=23.033333',
            '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
            '-c:a','aac','-shortest',str(source)],check=True)
        r=compose(source,out,sha256(source))
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(out),'-f','null','-'],check=True)
        assert r['video']=='h264' and r['audio']=='aac'
        print('PASS: synthetic 23-second full decode, H264/AAC')

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--source');a.add_argument('--out');a.add_argument('--source-sha256');a.add_argument('--genre',default='ai_work');a.add_argument('--smoke',action='store_true')
    args=a.parse_args()
    if args.smoke:smoke()
    else:print(json.dumps(compose(args.source,args.out,args.source_sha256,args.genre),ensure_ascii=False,indent=2))
