"""cycle1076: 3-beat Writer prompt-review animation (original vectors only).

Human-review-only overlay: purpose -> condition -> output format.
The real Writer screenshot remains a *static screenshot*, not a recorded operation.
No speech, subtitles, personal media or other scene layers are modified intentionally.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1080, 1920, 30
START, END = 520, 609  # scene 07: 17.333–20.300s, 89 frames
X, Y, OW, OH = 87, 454, 60, 246
# x=87..147: Writer's left margin. Text starts at x=154; subtitles start y>=1280.
PALETTES = {
    'ai_work': (34, 211, 202), 'finance': (242, 195, 106),
    'education': (117, 168, 252), 'health': (120, 224, 172),
    'travel': (248, 169, 187), 'beauty': (213, 166, 251),
    'food': (255, 166, 115), 'career': (112, 206, 239),
    'productivity': (184, 226, 113), 'lifestyle': (246, 201, 126),
}
CHECK_Y = (58, 122, 187)  # Writer lines purpose / condition / output format

def sha256(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1<<20), b''): h.update(part)
    return h.hexdigest()

def probe(path):
    raw = subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    d = json.loads(raw)
    v = next(s for s in d['streams'] if s['codec_type']=='video')
    a = next(s for s in d['streams'] if s['codec_type']=='audio')
    return {'video':v['codec_name'],'width':v['width'],'height':v['height'],
            'fps':v['r_frame_rate'],'frames':int(v.get('nb_frames') or 0),
            'audio':a['codec_name'],'sample_rate':int(a['sample_rate']),
            'duration':float(d['format']['duration'])}

def ease(x):
    x=max(0.,min(1.,x));return x*x*(3-2*x)

def frame_overlay(frame, genre='ai_work'):
    if genre not in PALETTES: raise ValueError('unknown genre')
    if not START <= frame < END: raise ValueError('frame outside Writer scene')
    color = PALETTES[genre]
    t = (frame-START)/(END-START-1)
    im = Image.new('RGBA',(OW,OH),(0,0,0,0))
    d = ImageDraw.Draw(im)
    # A narrow gutter-only progress spine guides the eye without covering text.
    d.line((28,CHECK_Y[0],28,CHECK_Y[-1]),fill=(*color,110),width=5)
    for i,cy in enumerate(CHECK_Y):
        # Three distinct stages: first 0.12–0.31, second 0.39–0.58, third 0.66–0.85.
        phase=(t-(.10+i*.275))/.20
        a=ease(phase)
        if a <= 0: continue
        # Active ring breathes briefly, then settles to a compact check.
        pulse=math.sin(math.pi*max(0,min(1,phase)))**2
        radius=18 + 3*pulse
        d.ellipse((28-radius,cy-radius,28+radius,cy+radius),
                  fill=(*color,int(245*a)),outline=(255,255,255,int(235*a)),width=3)
        # Animated check draws in two strokes; the later stage cannot appear first.
        first=ease(phase/.48)
        second=ease((phase-.40)/.48)
        if first>0:
            d.line((16,cy,16+11*first,cy+10*first),fill=(7,34,46,int(255*a)),width=5)
        if second>0:
            d.line((27,cy+10,27+13*second,cy+10-19*second),fill=(7,34,46,int(255*a)),width=5)
    # Do not flash at the cut: subtle fade at the first/last 5 frames.
    fade=ease(t/.055)*(1-ease((t-.945)/.055))
    if fade<1: im.putalpha(im.getchannel('A').point(lambda v:int(v*fade)))
    return im

def compose(source,out,expected_sha,genre='ai_work',short_smoke=False):
    if genre not in PALETTES:raise ValueError('unknown genre')
    if sha256(source)!=expected_sha:raise ValueError('source SHA256 mismatch; fail closed')
    p=probe(source)
    if (p['video'],p['width'],p['height'],p['fps'],p['audio'],p['sample_rate']) != ('h264',W,H,'30/1','aac',48000):
        raise ValueError('unsupported source streams')
    if not short_smoke and abs(p['duration']-23.033333)>.08:raise ValueError('unexpected source duration')
    if short_smoke and p['duration'] < END/FPS: raise ValueError('synthetic source too short')
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        for f in range(START,END):
            frame_overlay(f,genre).save(root/f'{f:04d}.png',compress_level=1)
        Path(out).parent.mkdir(parents=True,exist_ok=True)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-start_number',str(START),'-i',str(root/'%04d.png'),
             '-filter_complex',f'[1:v]format=rgba,setpts=PTS+{START}/{FPS}/TB[art];'
             f'[0:v][art]overlay=x={X}:y={Y}:eof_action=pass:shortest=0:format=auto[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
             '-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(out)]
        subprocess.run(cmd,check=True)
    return probe(out)

def smoke():
    # Synthetic source only. Does not distribute any actual video/media.
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);src=root/'synthetic.mp4';out=root/'review.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
            '-f','lavfi','-i','color=c=#071829:s=1080x1920:r=30:d=21',
            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=21',
            '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
            '-c:a','aac','-shortest',str(src)],check=True)
        result=compose(src,out,sha256(src),short_smoke=True)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(out),'-f','null','-'],check=True)
        assert result['video']=='h264' and result['audio']=='aac'
        print('PASS synthetic 21s full A/V decode; no private assets')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source');ap.add_argument('--out');ap.add_argument('--source-sha256')
    ap.add_argument('--genre',default='ai_work');ap.add_argument('--smoke',action='store_true')
    a=ap.parse_args()
    if a.smoke:smoke()
    else:print(json.dumps(compose(a.source,a.out,a.source_sha256,a.genre),ensure_ascii=False,indent=2))
