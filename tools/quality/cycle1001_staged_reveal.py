#!/usr/bin/env python3
"""Cycle1001: staged BEFORE-to-AFTER reveal for review-only vertical shorts.

Temporary mask over AFTER panel fades out, preserving original baked subtitles
and audio. Uses local FFmpeg and Pillow only; 10 reusable genre accent presets.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

SIZE=(1080,1920)
AFTER=(87,948,993,1244)
ACCENTS={
 'ai_work':'#2ADDD0','business':'#4CBCE8','finance':'#48DBA9',
 'education':'#66B7FF','health':'#56DDB6','travel':'#F6BD76',
 'cooking':'#FFAB7B','lifestyle':'#E8A8F4','technology':'#4EE0F0',
 'entertainment':'#FF9FC3'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def make_mask(genre='ai_work'):
    if genre not in ACCENTS: raise ValueError('unknown genre')
    if not Path(BOLD).is_file(): raise FileNotFoundError(BOLD)
    im=Image.new('RGBA',SIZE,(0,0,0,0)); d=ImageDraw.Draw(im)
    accent=ACCENTS[genre]
    d.rounded_rectangle(AFTER,radius=22,fill=(6,23,42,255),outline=accent,width=4)
    d.rounded_rectangle((113,970,321,1027),radius=12,fill=accent)
    d.text((140,975),'AFTER',font=ImageFont.truetype(BOLD,30),fill=(6,23,42))
    d.text((133,1050),'改善案を具体化',font=ImageFont.truetype(BOLD,51),fill='white')
    d.text((134,1137),'対象  →  条件  →  形式',font=ImageFont.truetype(FONT,35),fill=accent)
    return im

def render(source:Path,target:Path,genre='ai_work',start=14.5,hold=0.60,fade=0.65,mask_file=None):
    if not source.is_file(): raise FileNotFoundError(source)
    if min(start,hold,fade)<0 or fade==0: raise ValueError('invalid reveal timing')
    target.parent.mkdir(parents=True,exist_ok=True)
    mask=Path(mask_file) if mask_file else target.with_suffix('.mask.png')
    make_mask(genre).save(mask)
    filt=(f'[1:v]format=rgba,fade=t=out:st={hold:.3f}:d={fade:.3f}:alpha=1,'
          f'setpts=PTS+{start:.3f}/TB[cover];'
          '[0:v][cover]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-i',str(source),'-loop','1','-framerate','30','-i',str(mask),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(target)]
    subprocess.run(cmd,check=True)
    return {'start':start,'hold':hold,'fade':fade,'genre':genre,'panel':AFTER,'audio':'streamcopy'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--genre',choices=ACCENTS,default='ai_work')
    p.add_argument('--start',type=float,default=14.5)
    p.add_argument('--hold',type=float,default=.6)
    p.add_argument('--fade',type=float,default=.65)
    a=p.parse_args()
    print(render(a.input,a.output,a.genre,a.start,a.hold,a.fade))
