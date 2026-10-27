"""cycle914: original kinetic first-three-second hook, review-only reimplementation.
No reference images, customer data, brand impersonation or external footage embedded.
Only source media from a private approved-for-internal-review path is read.
"""
from __future__ import annotations
import argparse, hashlib, math, subprocess
from pathlib import Path

FPS=30; FRAMES=87; W=1080; H=1920; TOP=115; ART_H=1170; CAPTION_START=1490
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES={
 'ai_work':('#54e5eb','月別売上 / 架空の例','6月の入力が未完了'),
 'business':('#90baff','業務データ / 架空の例','入力の抜けを確認'),
 'learning':('#c6a5ff','学習記録 / 架空の例','未記入を確認'),
 'health':('#74d8b3','習慣記録 / 架空の例','記録の空欄を確認'),
 'beauty':('#ffb4d2','記録表 / 架空の例','未記入を確認'),
 'travel':('#71d7ff','旅程表 / 架空の例','未記入を確認'),
 'money':('#9be8a6','家計表 / 架空の例','未記入を確認'),
 'cooking':('#ffc68b','材料表 / 架空の例','未記入を確認'),
 'pets':('#ffe28e','お世話記録 / 架空の例','未記入を確認'),
 'entertainment':('#efb6ff','企画表 / 架空の例','未記入を確認'),
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha256(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def smooth(x:float)->float:
 x=max(0.,min(1.,x));return x*x*(3-2*x)

def phase(i:int)->int:
 if not 0<=i<FRAMES:raise ValueError('frame outside hook')
 return 0 if i<32 else 1 if i<61 else 2

def validate(src:Path,dst:Path,expected:str,genre:str,policy:str=POLICY):
 if policy!=POLICY:raise ValueError('review-only policy required')
 if genre not in GENRES:raise ValueError('unsupported genre')
 if not src.is_file() or sha256(src)!=expected:raise ValueError('source SHA mismatch')
 if src.resolve()==dst.resolve():raise ValueError('source overwrite forbidden')
 if not dst.name.endswith('REVIEW_ONLY.mp4'):raise ValueError('review-only output name required')
 if TOP+ART_H>=CAPTION_START:raise ValueError('caption safety violated')

def make_background():
 import numpy as np
 from PIL import Image,ImageDraw,ImageFilter
 y,x=np.mgrid[0:ART_H,0:W]
 r=(8+14*y/ART_H+9*x/W).clip(0,255)
 g=(22+22*y/ART_H+3*x/W).clip(0,255)
 b=(48+31*y/ART_H).clip(0,255)
 bg=Image.fromarray(np.dstack((r,g,b)).astype('uint8'),'RGB').convert('RGBA')
 glow=Image.new('RGBA',(W,ART_H));d=ImageDraw.Draw(glow)
 for cx,cy,rad,col in [(150,350,150,(15,226,234,48)),(860,260,185,(255,184,92,40)),(680,910,170,(40,108,255,38)),(280,1100,210,(245,163,83,34))]:
  d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=col)
 bg=Image.alpha_composite(bg,glow.filter(ImageFilter.GaussianBlur(85)))
 return bg

def draw_frame(i:int,genre:str,background,fonts):
 from PIL import Image,ImageDraw
 accent,heading,warning=GENRES[genre]
 fbig,flarge,fmed,fsmall=fonts
 img=background.copy();d=ImageDraw.Draw(img)
 p=phase(i);t=i/(FRAMES-1)
 d.rounded_rectangle((45,48,1035,1100),radius=46,fill=(5,14,33,255),outline=(95,161,187,130),width=3)
 d.rounded_rectangle((80,88,580,151),radius=25,fill=(13,74,94,255),outline=accent,width=2)
 d.text((105,96),'AI × 仕事術 / 3秒で伝える',font=fsmall,fill='white')
 bump=1.0+0.07*(1-smooth(min(1.,i/12)))
 text='これ、まだ' if p==0 else '見落としてない？'
 bbox=d.textbbox((0,0),text,font=fbig);tw=bbox[2]-bbox[0]
 d.text(((W-tw)/2,200),text,font=fbig,fill='white',stroke_width=2,stroke_fill='#092038')
 text2='手でやってるの？' if p==0 else 'データの空欄'
 bbox=d.textbbox((0,0),text2,font=flarge);tw=bbox[2]-bbox[0]
 d.text(((W-tw)/2,304),text2,font=flarge,fill='#ffd074' if p==0 else '#72f1f3',stroke_width=2,stroke_fill='#101929')
 d.rounded_rectangle((86,470,1006,1016),radius=31,fill=(2,16,36,255),outline=(99,199,222,180),width=4)
 d.text((121,505),heading,font=fmed,fill='white')
 for row,(month,a,b) in enumerate([('4月','12','8'),('5月','16','9'),('6月','—','—')]):
  y0=660+row*102
  bg=(12,61,82,255) if row%2==0 else (9,39,60,255)
  d.rounded_rectangle((116,y0,976,y0+84),radius=14,fill=bg)
  for x,val in [(155,month),(505,a),(808,b)]:
   d.text((x,y0+15),val,font=fmed,fill='white')
 d.rounded_rectangle((115,590,976,647),radius=13,fill=(17,78,103,250))
 for x,val in [(155,'月'),(500,'営業A'),(802,'営業B')]:d.text((x,596),val,font=fsmall,fill='white')
 if p>=1:
  alpha=int(90+165*smooth((i-32)/14))
  d.rounded_rectangle((112,861,980,956),radius=18,outline='#ffcf71',width=8)
  d.rounded_rectangle((668,490,980,568),radius=20,fill=(101,44,23,255),outline='#ffcf71',width=3)
  d.text((688,500),'6月 未入力',font=fsmall,fill='#ffdc99')
 if p==2:
  reveal=smooth((i-61)/14)
  x=110;y=1030
  d.rounded_rectangle((x,y,x+860,y+70),radius=18,fill=(9,78,83,255),outline=accent,width=3)
  d.text((x+27,y+7),'次のシーンで元データを照合',font=fsmall,fill='white')
 d.rounded_rectangle((96,1130,984,1141),radius=5,fill=(32,72,95,255))
 d.rounded_rectangle((96,1130,96+int(888*(i+1)/FRAMES),1141),radius=5,fill=accent)
 return img

def draw_frames(directory:Path,genre:str):
 from PIL import ImageFont
 directory.mkdir(parents=True,exist_ok=True)
 fonts=(ImageFont.truetype(FONT,75),ImageFont.truetype(FONT,72),ImageFont.truetype(FONT,38),ImageFont.truetype(REG,31))
 bg=make_background()
 for i in range(FRAMES):
  im=draw_frame(i,genre,bg,fonts)
  im.save(directory/f'{i:03d}.png',compress_level=2)

def render(src:Path,dst:Path,expected:str,genre:str,frames:Path):
 validate(src,dst,expected,genre)
 draw_frames(frames,genre)
 dst.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-framerate','30','-i',str(frames/'%03d.png'),'-filter_complex',f'[0:v][1:v]overlay=0:{TOP}:eof_action=pass:shortest=0:format=auto:enable=between(t\\,0\\,{(FRAMES-1)/FPS})[v]','-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','21','-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',str(dst)]
 subprocess.run(cmd,check=True)
 return dst

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--expected-sha',required=True);p.add_argument('--genre',choices=sorted(GENRES),default='ai_work');p.add_argument('--frames',type=Path,required=True)
 a=p.parse_args();print(render(a.source,a.output,a.expected_sha,a.genre,a.frames))
if __name__=='__main__':main()
