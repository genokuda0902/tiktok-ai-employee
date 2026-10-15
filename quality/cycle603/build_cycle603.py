#!/usr/bin/env python3
"""Cycle603: original, genre-colored, first-second CPU focus cue.

Zero external assets/APIs. Inherited baseline audio/art remain HUMAN_REVIEW.
No posting, no auto-merge, no paid services. Needs Pillow and FFmpeg.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'assets/cycle602_baseline.mp4'
GENRES=ROOT/'assets/genres.json'
OUTPUT=ROOT/'output/cycle603_FOCAL_HOOK_HUMAN_REVIEW.mp4'
FPS=30
FRAME_COUNT=54
REGION=(345,520,420,350)
DURATION=15.6

def accent_for(genre):
    cfg=json.loads(GENRES.read_text(encoding='utf-8'))['genres']
    if genre not in cfg: raise ValueError(f'Unknown genre: {genre}')
    s=cfg[genre]['theme'].lstrip('#')
    return tuple(int(s[i:i+2],16) for i in (0,2,4))

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def draw_cue(frame,accent):
    t=frame/FPS
    a=min(1.,max(0.,(t-.05)/.16),max(0.,(1.75-t)/.40))
    a=a*a*(3-2*a)
    w,h=REGION[2:]
    out=Image.new('RGBA',(w,h),(0,0,0,0))
    if a<=0:return out
    d=ImageDraw.Draw(out,'RGBA')
    x0,y0,x1,y1=51,43,359,306
    c=accent
    for x,dx in ((x0,1),(x1,-1)):
        for y,dy in ((y0,1),(y1,-1)):
            d.line([(x,y+dy*36),(x,y),(x+dx*36,y)],fill=(*c,round(185*a)),width=4,joint='curve')
    scan=Image.new('RGBA',(w,h),(0,0,0,0))
    s=ImageDraw.Draw(scan,'RGBA')
    sx=round(58+(t/1.8)*290)
    s.line((sx,66,sx,284),fill=(*c,round(70*a)),width=5)
    scan=scan.filter(ImageFilter.GaussianBlur(12))
    return Image.alpha_composite(out,scan)

def run(genre='雑学・科学',output=None):
    out=Path(output) if output else OUTPUT
    out.parent.mkdir(parents=True,exist_ok=True)
    accent=accent_for(genre)
    if not BASE.is_file():raise FileNotFoundError(BASE)
    with tempfile.TemporaryDirectory(prefix='cycle603_frames_') as td:
        td=Path(td)
        for i in range(FRAME_COUNT):
            draw_cue(i,accent).save(td/f'cue_{i:03d}.png')
        flt=f'[0:v][1:v]overlay=x={REGION[0]}:y={REGION[1]}:eof_action=pass:repeatlast=0:format=auto[v]'
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','1',
             '-i',str(BASE),'-framerate',str(FPS),'-i',str(td/'cue_%03d.png'),
             '-filter_complex',flt,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-threads','1','-preset','veryfast','-crf','18',
             '-pix_fmt','yuv420p','-c:a','copy','-t',str(DURATION),
             '-movflags','+faststart',str(out)]
        subprocess.run(cmd,check=True,timeout=240)
    print(json.dumps({'output':str(out),'sha256':sha256(out),'bytes':out.stat().st_size,'genre':genre},ensure_ascii=False))
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--genre',default='雑学・科学')
    p.add_argument('--output')
    args=p.parse_args();run(args.genre,args.output)
