#!/usr/bin/env python3
"""cycle613: larger Japanese one-line takeaway cards in mobile-safe area.

All imagery is original Pillow vector/text. Preserves inherited video/audio;
never posts, approves, or calls paid services. Run from any working directory.
"""
from __future__ import annotations
import argparse, json, hashlib, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'assets/cycle612_baseline.mp4'
GENRES=ROOT/'assets/genres.json'
OUT=ROOT/'output/cycle613_MOBILE_READABILITY_HUMAN_REVIEW.mp4'
FPS=30
W,H=1080,1920
STARTS=[0,70,136,178,247,287,352,415,468]
# x<=860 keeps the right-side TikTok UI region clear; y=1472 is below
# inherited speech captions (980..1248) and above the circuit decoration.
PX,PY,PW,PH=57,1472,810,208
TEXTS=[
 '小さくても、立派なPC',
 'カードほどのサイズ感',
 'モニターにつないで使う',
 '接続 → 電源 → 操作',
 'LEDを光らせてみよう',
 '入力が動作につながる',
 '自分だけの作品を作る',
 '気になったら保存して試す',
]
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1<<20),b''):h.update(block)
 return h.hexdigest()

def theme_color(genre):
 genres=json.loads(GENRES.read_text(encoding='utf-8'))['genres']
 if len(genres)!=10 or genre not in genres: raise ValueError('Unknown genre or invalid 10-genre config')
 return tuple(bytes.fromhex(genres[genre]['theme'].lstrip('#')))

def draw_panel(scene:int,genre='雑学・科学'):
 """810x208 RGBA card with opaque backing that completely hides old small card."""
 if not 0<=scene<8:raise ValueError('scene must be 0..7')
 rgb=theme_color(genre)
 scale=2
 im=Image.new('RGBA',(PW*scale,PH*scale),(0,0,0,0)); d=ImageDraw.Draw(im)
 def box(coords,fill,outline=None,width=2,r=0):
  coords=tuple(round(v*scale) for v in coords)
  d.rounded_rectangle(coords,radius=r*scale,fill=fill,outline=outline,width=width*scale)
 def text(x,y,t,font,fill):d.text((x*scale,y*scale),t,font=font,fill=fill,stroke_width=0)
 box((0,0,PW-1,PH-1),(3,15,27,255),(*rgb,255),2,21)
 box((10,11,PW-11,PH-11),(5,24,36,255),(*rgb,72),1,15)
 box((17,21,24,PH-22),(*rgb,255),r=3)
 reg=ImageFont.truetype(FONT_REG,26*scale)
 bold_size=55
 bold=ImageFont.truetype(FONT_BOLD,bold_size*scale)
 while d.textbbox((0,0),TEXTS[scene],font=bold)[2]>705*scale and bold_size>38:
  bold_size-=1; bold=ImageFont.truetype(FONT_BOLD,bold_size*scale)
 text(43,20,'ここだけ覚える',reg,(*rgb,255))
 text(668,20,f'{scene+1:02d} / 08',reg,(174,206,208,255))
 text(43,69,TEXTS[scene],bold,(245,252,252,255))
 for j in range(8):
  left=45+j*91
  box((left,173,left+74,180),(*rgb,255) if j<=scene else (67,89,99,255),r=3)
 return im.resize((PW,PH),Image.Resampling.LANCZOS)

def render(source=BASE,output=OUT,genre='雑学・科学'):
 source=Path(source);output=Path(output)
 if not source.is_file():raise FileNotFoundError(source)
 theme_color(genre)
 output.parent.mkdir(parents=True,exist_ok=True)
 panels=output.parent/'panels';panels.mkdir(exist_ok=True)
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
 for j in range(8):
  p=panels/f'takeaway_{j+1:02}.png';draw_panel(j,genre).save(p)
  args+=['-loop','1','-framerate',str(FPS),'-i',str(p)]
 filters=[];last='0:v'
 for j in range(8):
  nxt=f'o{j+1}'
  filters.append(f"[{last}][{j+1}:v]overlay=x={PX}:y={PY}:shortest=0:eof_action=pass:enable='between(n,{STARTS[j]},{STARTS[j+1]-1})':format=auto[{nxt}]")
  last=nxt
 filters.append(f'[{last}]trim=end_frame=468,setpts=PTS-STARTPTS[vout]')
 args+=['-filter_complex',';'.join(filters),'-map','[vout]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
 subprocess.run(args,check=True,timeout=240)
 return {'output':str(output),'sha256':digest(output),'genre':genre,'scenes':8,'status':'HUMAN_REVIEW','publication':'NOT_APPROVED'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=BASE);p.add_argument('--output',type=Path,default=OUT);p.add_argument('--genre',default='雑学・科学')
 a=p.parse_args();print(json.dumps(render(a.input,a.output,a.genre),ensure_ascii=False))
