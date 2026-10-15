#!/usr/bin/env python3
"""Cycle602: fill unused lower third with restrained ambient-circuit art.

Fully offline, 10-genre accent themes. Inherited video/audio remain review-only.
No third-party imagery, no automatic posting. Requires Pillow, numpy, ffmpeg.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'assets/cycle601_baseline.mp4'
GENRES=ROOT/'assets/genres.json'
OUT=ROOT/'output/cycle602_AMBIENT_CANVAS_HUMAN_REVIEW.mp4'
W,H=1080,1920
ART_W,ART_H=1160,670
START_Y=1250
FPS=30
DURATION=15.6

def accent_for(genre):
    config=json.loads(GENRES.read_text(encoding='utf-8'))['genres']
    if genre not in config: raise ValueError(f'unknown genre {genre}')
    s=config[genre]['theme'].lstrip('#')
    return tuple(int(s[i:i+2],16) for i in (0,2,4))

def create_ambient(genre='雑学・科学'):
    accent=np.array(accent_for(genre),dtype=float)
    yy,xx=np.mgrid[0:ART_H,0:ART_W]
    base=np.array([1,9,21],dtype=float)
    glow1=np.exp(-(((xx-330)/410)**2+((yy-355)/270)**2)*1.2)
    glow2=np.exp(-(((xx-990)/310)**2+((yy-555)/240)**2)*1.25)
    val=np.zeros((ART_H,ART_W,3),dtype=np.float32)
    for ch in range(3):
        val[:,:,ch]=base[ch]+(accent[ch]*0.20+5)*glow1+(accent[ch]*0.09+4)*glow2
    rng=np.random.default_rng(602)
    val+=rng.normal(0,0.65,(ART_H,ART_W,1))
    rgb=np.uint8(np.clip(val,0,255))
    art=Image.fromarray(rgb,'RGB').convert('RGBA')
    d=ImageDraw.Draw(art,'RGBA')
    c=tuple(int(i) for i in accent)
    paths=[[(35,310),(170,310),(170,390),(400,390),(400,450),(580,450)],
           [(75,550),(270,550),(270,485),(485,485),(485,575),(650,575)],
           [(1130,320),(980,320),(980,420),(790,420),(790,505),(610,505)],
           [(1100,620),(970,620),(970,555),(830,555)],
           [(90,640),(180,640),(180,600),(340,600)]]
    for pts in paths:
        d.line(pts,fill=(*c,34),width=2,joint='curve')
        for x,y in [pts[0],pts[-1]]:
            d.ellipse((x-5,y-5,x+5,y+5),fill=(*c,64))
            d.ellipse((x-2,y-2,x+2,y+2),fill=(*c,130))
    for i in range(38):
        x=int(70+(i*157)%1020); y=int(250+(i*113)%390)
        d.ellipse((x-1,y-1,x+1,y+1),fill=(*c,36))
    arr=np.asarray(art).copy()
    fade=np.clip((np.arange(ART_H)-8)/95,0,1)**1.5
    arr[:,:,3]=np.uint8(fade[:,None]*255)
    return Image.fromarray(arr,'RGBA')

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def run(genre='雑学・科学',output=None):
    out=Path(output) if output else OUT
    out.parent.mkdir(parents=True,exist_ok=True)
    if not BASE.exists():raise FileNotFoundError(BASE)
    art=create_ambient(genre)
    art_path=out.parent/'ambient_circuit.png'
    art.save(art_path)
    flt=(f"[0:v][1:v]overlay=x='-40+24*sin(t*0.42)':y={START_Y}:"
         "eval=frame:shortest=1:format=auto[v]")
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','1',
         '-i',str(BASE),'-loop','1','-framerate',str(FPS),'-i',str(art_path),
         '-filter_complex',flt,'-map','[v]','-map','0:a:0',
         '-c:v','libx264','-threads','1','-preset','veryfast','-crf','18',
         '-pix_fmt','yuv420p','-c:a','copy','-t',str(DURATION),
         '-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True,timeout=180)
    print(json.dumps({'output':str(out),'bytes':out.stat().st_size,'sha256':sha256(out)},ensure_ascii=False))
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--genre',default='雑学・科学')
    p.add_argument('--output')
    a=p.parse_args();run(a.genre,a.output)
