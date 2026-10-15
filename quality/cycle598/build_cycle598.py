#!/usr/bin/env python3
"""Cycle598: Japanese scene-aware keyword cards in a lower UI-safe zone. No posting."""
from __future__ import annotations
import argparse, json, subprocess, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'assets/cycle597_baseline.mp4'
OUT=ROOT/'output/cycle598_KEYWORD_SAFEZONE_HUMAN_REVIEW.mp4'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
CARD_W,CARD_H=800,220
X,Y=52,1445
SCENES=[
  (0.0,2.3,'小さなPC','発見'),
  (2.3,4.5,'カードサイズ','比較'),
  (4.5,7.3,'モニター接続','使い方'),
  (7.3,8.5,'プログラミング','使い方'),
  (8.5,9.5,'電子工作','活用'),
  (9.5,11.7,'入力 → 判断 → 動作','自動化'),
  (11.7,13.9,'作品づくり','実践'),
  (13.9,15.6,'保存して後で試す','保存'),
]
GENRE='雑学・科学'
ACCENT=(73,226,200)

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def font(size,bold=False):
 return ImageFont.truetype(BOLD if bold else FONT,size)

def make_card(keyword, category, accent=ACCENT):
 """800x220 RGBA card; composited at x52..852, y1445..1665."""
 im=Image.new('RGBA',(CARD_W,CARD_H),(0,0,0,0))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((8,8,CARD_W-8,174),radius=26,fill=(4,22,36,237),outline=(*accent,188),width=3)
 d.rounded_rectangle((24,20,31,155),radius=4,fill=(*accent,255))
 d.text((53,18),'1秒で覚えるキーワード',font=font(24),fill=(171,206,215,255))
 d.rounded_rectangle((CARD_W-148,20,CARD_W-35,61),radius=14,fill=(22,67,75,255))
 fs=24
 while d.textbbox((0,0),category,font=font(fs))[2] > 93 and fs>17:fs-=1
 d.text((CARD_W-138,23),category,font=font(fs),fill=(177,245,228,255))
 fs=58
 while d.textbbox((0,0),keyword,font=font(fs,True))[2] > CARD_W-110 and fs>30:fs-=2
 d.text((52,67),keyword,font=font(fs,True),fill=(248,252,254,255),stroke_width=0)
 d.rounded_rectangle((54,152,CARD_W-54,157),radius=2,fill=(*accent,210))
 d.text((10,188),'図解・CGイメージ｜音声・字幕は確認待ち',font=font(18),fill=(159,175,190,255))
 return im

def load_accent(genre):
 genres=json.loads((ROOT/'config/genres.json').read_text(encoding='utf-8'))['genres']
 if genre not in genres: raise ValueError(f'Unknown genre: {genre}')
 color=genres[genre]['theme'].lstrip('#')
 return tuple(int(color[i:i+2],16) for i in (0,2,4))

def run(genre=GENRE):
 accent=load_accent(genre)
 assert SRC.is_file(),f'Missing input: {SRC}'
 OUT.parent.mkdir(exist_ok=True)
 cards=ROOT/'output/cards';cards.mkdir(exist_ok=True)
 for i,(_,_,word,tag) in enumerate(SCENES[:-1]):make_card(word,tag,accent=accent).save(cards/f'card_{i+1:02d}.png')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(SRC)]
 for i in range(len(SCENES)-1):
  cmd+=['-loop','1','-framerate','30','-i',str(cards/f'card_{i+1:02d}.png')]
 chain=["[0:v]drawbox=x=0:y=1425:w=900:h=255:color=0x000b19:t=fill:enable='lt(t,13.9)'[masked]"]; prev='masked'
 for i,(a,b,_,_) in enumerate(SCENES[:-1],1):
  out=f'v{i}'
  chain.append(f"[{prev}][{i}:v]overlay=x={X}:y={Y}:enable='gte(t,{a})*lt(t,{b})':format=auto[{out}]")
  prev=out
 cmd+=['-filter_complex',';'.join(chain),'-map',f'[{prev}]','-map','0:a:0',
       '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
       '-c:a','copy','-t','15.6','-movflags','+faststart',str(OUT)]
 subprocess.run(cmd,check=True)
 print(json.dumps({'mp4':str(OUT),'sha256':sha(OUT),'bytes':OUT.stat().st_size},ensure_ascii=False))

if __name__=='__main__':
 parser=argparse.ArgumentParser()
 parser.add_argument('--genre',default=GENRE)
 run(parser.parse_args().genre)
