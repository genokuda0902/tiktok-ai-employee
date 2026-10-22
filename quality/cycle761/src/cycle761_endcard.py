#!/usr/bin/env python3
"""Review-only image-first 10-genre end card renderer.

Replaces the last three seconds of an explicitly SHA-allowlisted source MP4.
Uses only Pillow-generated synthetic graphics; preserves the original audio bitstream.
Does not publish or certify audio/caption sync or platform safe areas.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS = 1080,1920,30
CUT_FRAME=729
END_FRAMES=90
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES={
 'ai_work':'#35E3DA','romance':'#E7A2F4','beauty':'#F4A3C4',
 'money':'#9AE5A5','trivia':'#65BFF9','gadgets':'#F3AE78',
 'health':'#A5DCA4','sales':'#F4C96C','travel':'#72DBE5','mystery':'#C3B2F6'
}
RIGHT_SAFE=880

def sha256(path:Path)->str:
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def font(size,bold=True):return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)
def validate(cfg):
 if cfg.get('genre') not in GENRES:raise ValueError('unknown genre')
 if cfg.get('asset_rights')!='synthetic_local_only':raise ValueError('asset rights must be synthetic_local_only')
 if cfg.get('approval')!='HUMAN_REVIEW':raise ValueError('human review required')
 for k in ('title','subtitle','proof','caption','disclaimer'):
  if not isinstance(cfg.get(k),str) or not 1<=len(cfg[k])<=40:raise ValueError('invalid '+k)
 if len(cfg.get('steps',[]))!=3 or any(not isinstance(s,str) or len(s)>19 for s in cfg['steps']):raise ValueError('three short steps required')
 if any('\n' in x or '\r' in x for x in cfg['steps']):raise ValueError('invalid step')
 return cfg

def txt(d,xy,s,size,color='#FFFFFF',bold=True,stroke=0):
 d.text(xy,s,font=font(size,bold),fill=color,stroke_width=stroke,stroke_fill='#091726')

def create_background(accent):
 im=Image.new('RGB',(W,H));pix=im.load()
 for y in range(H):
  for x in range(W):
   n=math.exp(-((x-190)**2/(520**2)+(y-350)**2/(550**2)))
   n2=math.exp(-((x-840)**2/(560**2)+(y-1100)**2/(780**2)))
   pix[x,y]=(int(4+10*n+3*n2),int(14+18*n+7*n2),int(28+25*n+14*n2))
 d=ImageDraw.Draw(im,'RGBA')
 for y in range(140,1660,100):d.line((40,y,970,y),fill=(80,160,205,12),width=1)
 for x in range(60,1020,100):d.line((x,100,x,1690),fill=(80,160,205,10),width=1)
 glow=Image.new('RGBA',(W,H));g=ImageDraw.Draw(glow)
 g.ellipse((-200,-200,600,650),fill=(*accent,42))
 glow=glow.filter(ImageFilter.GaussianBlur(135))
 return Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB')

def render_frame(base,cfg,i):
 t=i/FPS; a=rgb(GENRES[cfg['genre']]);accent=GENRES[cfg['genre']]
 im=base.copy();d=ImageDraw.Draw(im,'RGBA')
 fade=min(1.,(i+1)/6)
 d.rounded_rectangle((68,135,861,217),radius=25,fill=(9,30,46,242),outline=(*a,150),width=3)
 txt(d,(94,148),'AI時短ラボ  /  保存用ガイド',38,accent)
 txt(d,(65,292),cfg['title'],72,'#FFFFFF')
 txt(d,(70,399),cfg['subtitle'],35,'#C2D4E4',False)
 for j,step in enumerate(cfg['steps']):
  y=560+j*185;shown=t>=0.38+j*0.57
  d.rounded_rectangle((66,y,861,y+145),radius=27,fill=(13,44,60,246) if shown else (8,25,40,225),outline=(*a,230) if shown else (74,104,132,135),width=4 if shown else 2)
  d.rounded_rectangle((91,y+33,166,y+110),radius=19,fill=(*a,255) if shown else (43,70,88,255))
  txt(d,(113,y+43),str(j+1),44,'#061824' if shown else '#C4D5E0')
  txt(d,(189,y+43),step,43,'#FFFFFF' if shown else '#90A9BD')
 d.rounded_rectangle((66,1152,861,1353),radius=30,fill=(5,27,42,255),outline=(*a,185),width=3)
 txt(d,(93,1181),cfg['proof'],43,accent)
 txt(d,(94,1266),'※ 数値は架空の例です',29,'#B4C5D6',False)
 d.rounded_rectangle((66,1400,861,1412),radius=6,fill=(39,66,80,255))
 d.rounded_rectangle((66,1400,66+int(795*min(1,(t+0.03)/2.7)),1412),radius=6,fill=(*a,255))
 d.rounded_rectangle((66,1480,861,1663),radius=28,fill=(4,16,29,255),outline=(*a,215),width=3)
 txt(d,(106,1520),cfg['caption'],62,'#FFFFFF')
 txt(d,(72,1701),cfg['disclaimer'],26,'#AFC3D2',False)
 if fade<1:
  dark=Image.new('RGBA',(W,H),(0,0,0,round(255*(1-fade))))
  im=Image.alpha_composite(im.convert('RGBA'),dark).convert('RGB')
 return im

def run(source:Path,config:Path,out:Path,expected_sha:str,frames:Path):
 cfg=validate(json.loads(config.read_text(encoding='utf8')))
 if not source.is_file() or sha256(source)!=expected_sha:raise ValueError('input missing or SHA256 mismatch')
 if source.resolve()==out.resolve():raise ValueError('input overwrite forbidden')
 frames.mkdir(parents=True,exist_ok=True);out.parent.mkdir(parents=True,exist_ok=True)
 base=create_background(rgb(GENRES[cfg['genre']]))
 for i in range(END_FRAMES):render_frame(base,cfg,i).save(frames/f'{i:04}.jpg',quality=91,subsampling=0)
 cmd=['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error','-i',str(source),'-framerate',str(FPS),'-i',str(frames/'%04d.jpg'),'-filter_complex',
      f'[0:v]trim=end_frame={CUT_FRAME},setpts=PTS-STARTPTS[v0];[1:v]trim=end_frame={END_FRAMES},setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v]',
      '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(out)]
 subprocess.run(cmd,check=True,timeout=300)
 return {'cycle':761,'input_sha256':expected_sha,'output_sha256':sha256(out),'genre':cfg['genre'],'frames_replaced':END_FRAMES,'cut_frame':CUT_FRAME,'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--expected-sha',required=True);p.add_argument('--frames',type=Path,required=True)
 x=p.parse_args();print(json.dumps(run(x.source,x.config,x.output,x.expected_sha,x.frames),ensure_ascii=False,indent=2))
