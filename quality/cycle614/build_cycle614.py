#!/usr/bin/env python3
"""Cycle 614: 1.6-second CPU hero focus pulse, 10-theme reusable overlay.

No network, licensed content downloads, paid API, or posting. Uses inherited
cycle613 MP4 as a baseline, without claiming ownership of its underlying assets.
"""
from __future__ import annotations
import argparse, colorsys, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'assets/cycle613_baseline.mp4'
OUT=ROOT/'output/cycle614_HERO_FOCUS_PULSE_HUMAN_REVIEW.mp4'
GENRES=ROOT/'assets/genres.json'
FPS=30; PULSE_FRAMES=48; W,H=1080,1920
X,Y,SIZE=270,400,430

def sha256(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

def palette(genre):
 cfg=json.loads(GENRES.read_text(encoding='utf-8'))['genres']
 if len(cfg)!=10 or genre not in cfg: raise ValueError('Requires one of exactly ten configured genres')
 h=cfg[genre]['theme'].lstrip('#')
 return tuple(bytes.fromhex(h))

def pulse_frame(n,genre='雑学・科学'):
 """Transparent 430x430 RGBA, no text and no change outside CPU region."""
 if not 0<=n<PULSE_FRAMES: raise ValueError('frame outside focus sequence')
 col=palette(genre)
 scale=2; sz=SIZE*scale
 im=Image.new('RGBA',(sz,sz));d=ImageDraw.Draw(im)
 t=n/FPS
 fade=min(1,t/.22,(PULSE_FRAMES/FPS-t)/.24)
 fade=max(0,fade)
 breath=.72+.28*math.sin(2*math.pi*1.7*t)
 alpha=round(235*fade*breath)
 x0,y0,x1,y1=(62*scale,78*scale,357*scale,337*scale)
 length=33*scale
 for x,dx in ((x0,1),(x1,-1)):
  for y,dy in ((y0,1),(y1,-1)):
   d.line([(x+dx*length,y),(x,y),(x,y+dy*length)],fill=(*col,alpha),width=4*scale,joint='curve')
 edges=[(x0,y0,x1,y0),(x1,y0,x1,y1),(x1,y1,x0,y1),(x0,y1,x0,y0)]
 per=2*((x1-x0)+(y1-y0));dist=(t*per*.68)%per
 sx=sy=0
 for a,b,c,e in edges:
  L=math.hypot(c-a,e-b)
  if dist<=L:
   u=dist/L;sx=a+(c-a)*u;sy=b+(e-b)*u;break
  dist-=L
 glow=Image.new('RGBA',(sz,sz));g=ImageDraw.Draw(glow)
 r=11*scale
 g.ellipse((sx-r,sy-r,sx+r,sy+r),fill=(*col,round(160*fade)))
 glow=glow.filter(ImageFilter.GaussianBlur(13*scale))
 im=Image.alpha_composite(glow,im)
 d=ImageDraw.Draw(im)
 r2=4*scale
 d.ellipse((sx-r2,sy-r2,sx+r2,sy+r2),fill=(235,255,255,round(220*fade)))
 return im.resize((SIZE,SIZE),Image.Resampling.LANCZOS)

def render(source=BASE,output=OUT,genre='雑学・科学'):
 source=Path(source);output=Path(output)
 if not source.is_file():raise FileNotFoundError(source)
 palette(genre);output.parent.mkdir(parents=True,exist_ok=True)
 frames=output.parent/'pulse_frames';frames.mkdir(parents=True,exist_ok=True)
 for i in range(PULSE_FRAMES):pulse_frame(i,genre).save(frames/f'pulse_{i:03d}.png')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate',str(FPS),'-start_number','0','-i',str(frames/'pulse_%03d.png'),'-filter_complex',f'[0:v][1:v]overlay=x={X}:y={Y}:eof_action=pass:shortest=0:format=auto,trim=end_frame=468,setpts=PTS-STARTPTS[vout]','-map','[vout]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
 subprocess.run(cmd,check=True,timeout=240)
 return {'output':str(output),'sha256':sha256(output),'genre':genre,'quality':'HUMAN_REVIEW','publication':'NOT_APPROVED'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=BASE);p.add_argument('--output',type=Path,default=OUT);p.add_argument('--genre',default='雑学・科学')
 a=p.parse_args();print(json.dumps(render(a.input,a.output,a.genre),ensure_ascii=False))
