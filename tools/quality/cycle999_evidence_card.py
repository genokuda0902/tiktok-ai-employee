#!/usr/bin/env python3
"""Reusable review-only evidence-card overlay for image-first vertical shorts.

Only updates scene 6 central evidence area. Does not generate or modify speech,
subtitles, or any personal-data sources. Ten genre color presets are templates,
not ten independently tested videos.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

SIZE=(1080,1920)
CARD=(62,515,1018,1360)
GENRES={
 'ai_work':'#2ADDD0','business':'#4CBCE8','finance':'#48DBA9',
 'education':'#66B7FF','health':'#56DDB6','travel':'#F6BD76',
 'cooking':'#FFAB7B','lifestyle':'#E8A8F4','technology':'#4EE0F0',
 'entertainment':'#FF9FC3'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
EXAMPLE={
 'title':'修正は、1回に1点だけ',
 'before':'もっと良くして',
 'after1':'週次報告の「冒頭」だけ',
 'after2':'数字を残して、3行に短縮',
 'note':'対象と条件を指定すると、確認しやすい',
}

def font(px:int,bold:bool=False):
 return ImageFont.truetype(FONT_BOLD if bold else FONT,px)

def text_fit(draw,text,box,max_size=48,min_size=20,bold=False):
 x0,y0,x1,y1=box
 for size in range(max_size,min_size-1,-1):
  f=font(size,bold)
  b=draw.textbbox((0,0),text,font=f)
  if b[2]-b[0] <= x1-x0 and b[3]-b[1]<=y1-y0:
   return f
 raise ValueError('text does not fit')

def make_card(genre='ai_work',content=None):
 if genre not in GENRES: raise ValueError('unknown genre')
 c=dict(EXAMPLE if content is None else content)
 if set(c)!=set(EXAMPLE): raise ValueError('expected complete text keys')
 if any(not isinstance(v,str) or not v or len(v)>90 for v in c.values()):
  raise ValueError('invalid card text')
 accent=GENRES[genre]
 im=Image.new('RGBA',SIZE,(0,0,0,0));d=ImageDraw.Draw(im)
 d.rounded_rectangle(CARD,radius=35,fill=(5,17,37,252),outline=(62,91,117,255),width=3)
 d.rounded_rectangle((86,567,994,669),radius=20,fill=(17,43,64,255))
 d.rounded_rectangle((101,588,116,646),radius=7,fill=accent)
 d.text((136,585),c['title'],font=text_fit(d,c['title'],(136,582,966,654),max_size=47,bold=True),fill='white')
 d.rounded_rectangle((87,703,993,914),radius=22,fill=(47,30,40,255),outline=(188,95,102,255),width=3)
 d.rounded_rectangle((111,723,310,775),radius=13,fill=(143,53,65,255))
 d.text((139,727),'BEFORE',font=font(29,True),fill='white')
 d.text((127,795),c['before'],font=text_fit(d,c['before'],(127,791,952,878),max_size=51,bold=True),fill=(255,238,239))
 d.rounded_rectangle((87,948,993,1244),radius=22,fill=(18,51,62,255),outline=accent,width=4)
 d.rounded_rectangle((111,970,290,1024),radius=13,fill=accent)
 d.text((139,973),'AFTER',font=font(29,True),fill=(4,26,37))
 d.text((125,1041),c['after1'],font=text_fit(d,c['after1'],(125,1038,951,1112),max_size=43,bold=True),fill='white')
 d.text((125,1130),c['after2'],font=text_fit(d,c['after2'],(125,1128,951,1202),max_size=43,bold=True),fill=(116,245,223))
 d.rounded_rectangle((90,1267,991,1330),radius=13,fill=(12,36,53,255))
 d.text((118,1278),c['note'],font=text_fit(d,c['note'],(118,1275,959,1322),max_size=30),fill=(191,218,232))
 return im

def render(src:Path,dst:Path,genre='ai_work',start=14.5,end=17.15,overlay_path=None):
 if not src.is_file(): raise FileNotFoundError(src)
 if not (0<=start<end): raise ValueError('bad scene interval')
 dst.parent.mkdir(parents=True,exist_ok=True)
 png=overlay_path or dst.with_suffix('.overlay.png')
 make_card(genre).save(png)
 filt=f"[0:v][1:v]overlay=0:0:format=auto:shortest=1:enable='between(t,{start},{end})',format=yuv420p[v]"
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-loop','1','-framerate','30','-i',str(png),
      '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
      '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dst)]
 subprocess.run(cmd,check=True)
 return {'genre':genre,'scene':'06/08','start':start,'end':end,'overlay_bounds':CARD,'audio':'streamcopy'}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
 p.add_argument('--genre',choices=GENRES,default='ai_work')
 a=p.parse_args();print(render(a.input,a.output,a.genre))
