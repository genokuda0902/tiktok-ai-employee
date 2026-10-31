"""cycle1074: original ten-genre paper-stack -> organized-checklist animation.

REVIEW ONLY. Apply solely to a SHA256-verified source. This is NOT v33 code.
No user media is embedded or uploaded; captions and inherited AAC are untouched.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1080, 1920, 30
START, END = 87, 174  # 2.900 to 5.800 seconds; scene 02 only
X, Y, OW, OH = 620, 156, 440, 285
# The title occupies x<=570; task rows begin y>=465; subtitles y>=1280.
PALETTES = {
    'ai_work': (55, 227, 244), 'finance': (242, 195, 106),
    'education': (117, 168, 252), 'health': (120, 224, 172),
    'travel': (248, 169, 187), 'beauty': (213, 166, 251),
    'food': (255, 166, 115), 'career': (112, 206, 239),
    'productivity': (184, 226, 113), 'lifestyle': (246, 201, 126),
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def probe(path):
    raw = subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    d = json.loads(raw)
    v = next(s for s in d['streams'] if s['codec_type']=='video')
    a = next(s for s in d['streams'] if s['codec_type']=='audio')
    return {'video':v['codec_name'], 'width':v['width'], 'height':v['height'],
            'fps':v['r_frame_rate'], 'frames':int(v.get('nb_frames') or 0),
            'audio':a['codec_name'], 'sample_rate':int(a['sample_rate']),
            'duration':float(d['format']['duration'])}

def ease(t):
    t=max(0.,min(1.,t))
    return t*t*(3-2*t)

def _paper(color, kind):
    """Original vector icon; no font, third-party assets or text required."""
    p=Image.new('RGBA',(172,182),(0,0,0,0))
    d=ImageDraw.Draw(p)
    d.rounded_rectangle((5,5,167,177),radius=16,fill=(19,44,63,245),outline=(*color,230),width=3)
    d.rounded_rectangle((22,20,150,57),radius=9,fill=(*color,52))
    if kind==0:  # table
        for x in (39,68,97,126):d.line((x,27,x,50),fill=(*color,180),width=2)
        for y in (29,40,51):d.line((30,y,141,y),fill=(*color,180),width=2)
    elif kind==1:  # mail
        d.rounded_rectangle((41,25,130,52),radius=3,outline=(*color,235),width=3)
        d.line((42,27,85,44,129,27),fill=(*color,235),width=3)
    else:  # document
        d.line((49,27,126,27),fill=(*color,235),width=5)
        d.line((49,41,112,41),fill=(*color,235),width=4)
    for i,w in enumerate((113,98,119,76)):
        d.rounded_rectangle((29,78+i*20,29+w,83+i*20),radius=2,fill=(111,151,175,180))
    return p

def frame_overlay(frame, genre='ai_work'):
    if genre not in PALETTES:raise ValueError('unknown genre')
    if not START<=frame<END:raise ValueError('frame out of range')
    color=PALETTES[genre]
    t=(frame-START)/(END-START-1)
    enter=ease(t/.16)
    exit=1-ease((t-.87)/.13)
    alpha=max(0,min(1,enter*exit))
    im=Image.new('RGBA',(OW,OH),(0,0,0,0))
    # In the first half, three papers look scattered. In the second half,
    # they align into a neat stack; the motion is content-specific, not random zoom.
    align=ease((t-.31)/.50)
    positions=[(38,69,-10),(144,33,9),(240,73,-6)]
    targets=[(82,61,-2),(145,49,0),(208,37,2)]
    for i in range(3):
        px,py,ang=positions[i];tx,ty,ta=targets[i]
        x=px+(tx-px)*align+3*math.sin(t*6+i)*math.sin(math.pi*t)
        y=py+(ty-py)*align+3*math.sin(t*4+i)
        a=ang+(ta-ang)*align
        p=_paper(color,i)
        # Individual cards pop into the scene in three successive beats.
        appearance=ease((t-i*.11)/.22)
        if appearance<=0:continue
        p=p.rotate(a,Image.Resampling.BICUBIC,expand=True)
        shadow=Image.new('RGBA',p.size,(0,0,0,0))
        shadow.putalpha(p.getchannel('A').filter(ImageFilter.GaussianBlur(11)).point(lambda v:int(v*.43)))
        ix=int(x-(p.width-172)/2);iy=int(y-(p.height-182)/2)
        im.alpha_composite(shadow,(ix+8,iy+11))
        im.alpha_composite(p,(ix,iy))
    # Completion tick is revealed only once the three items are organized.
    done=ease((t-.73)/.18)
    if done>0:
        d=ImageDraw.Draw(im)
        cx,cy=348,225
        r=27*done
        d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(*color,int(215*done)))
        d.line([(cx-12*done,cy),(cx-2*done,cy+10*done),(cx+15*done,cy-12*done)],fill=(7,27,40,int(255*done)),width=6,joint='curve')
    if alpha<1:
        im.putalpha(im.getchannel('A').point(lambda v:int(v*alpha)))
    return im

def compose(source,out,expected_sha,genre='ai_work',short_smoke=False):
    if genre not in PALETTES:raise ValueError('unknown genre')
    if sha256(source)!=expected_sha:raise ValueError('SHA256 mismatch: source not approved for this run')
    p=probe(source)
    if (p['video'],p['width'],p['height'],p['fps'],p['audio'],p['sample_rate'])!=('h264',W,H,'30/1','aac',48000):
        raise ValueError('unsupported source format')
    if not short_smoke and abs(p['duration']-23.033333)>.08:raise ValueError('source duration mismatch')
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        for f in range(START,END):
            frame_overlay(f,genre).save(root/f'{f:04d}.png',compress_level=1)
        Path(out).parent.mkdir(parents=True,exist_ok=True)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-start_number',str(START),'-i',str(root/'%04d.png'),
             '-filter_complex',f'[1:v]format=rgba,setpts=PTS+{START}/{FPS}/TB[art];'
             f'[0:v][art]overlay=x={X}:y={Y}:eof_action=pass:shortest=0:format=auto[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),
             '-c:a','copy','-movflags','+faststart',str(out)]
        subprocess.run(cmd,check=True)
    return probe(out)

def smoke():
    # Fully synthetic 6s source, never private media in CI.
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);src=root/'source.mp4';out=root/'out.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
            '-f','lavfi','-i','color=c=#071829:s=1080x1920:r=30:d=6',
            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=6',
            '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
            '-c:a','aac','-shortest',str(src)],check=True)
        result=compose(src,out,sha256(src),short_smoke=True)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(out),'-f','null','-'],check=True)
        assert result['video']=='h264' and result['audio']=='aac'
        print('PASS: synthetic 6s H264/AAC full decode')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source');ap.add_argument('--out');ap.add_argument('--source-sha256')
    ap.add_argument('--genre',default='ai_work');ap.add_argument('--smoke',action='store_true')
    a=ap.parse_args()
    if a.smoke:smoke()
    else:print(json.dumps(compose(a.source,a.out,a.source_sha256,a.genre),ensure_ascii=False,indent=2))
