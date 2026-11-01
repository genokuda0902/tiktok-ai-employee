"""Reusable Japanese end-scene completion badge, with protected subtitle area.
Review-only: original/private source media are never committed or published.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRE_PALETTE = {
 'ai-work':'#50d9cf','finance':'#f3c96b','career':'#76d6ac',
 'health':'#76d6b6','learning':'#6fbdff','travel':'#f5b47b',
 'technology':'#79baff','business':'#51d6d2','life':'#eeadd0',
 'history':'#dfb77d'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def run(cmd):
 return subprocess.run(cmd,check=True,capture_output=True,text=True)

def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format',
                         '-of','json',str(path)]).stdout)

def validate_overlay(x,y,w,h,width,height,caption_top):
 if min(x,y)<0 or min(w,h)<=0 or x+w>width or y+h>height:
  raise ValueError('Overlay outside frame')
 if y+h>caption_top:
  raise ValueError('Overlay intrudes into protected Japanese caption region')
 return True

def make_step_card(path,genre='ai-work',step='03',title='ステップ完了',width=290,height=72):
 if genre not in GENRE_PALETTE: raise ValueError('Unknown genre')
 if len(step)>3 or len(title)>9: raise ValueError('Text too long')
 img=Image.new('RGBA',(width,height),(0,0,0,0))
 d=ImageDraw.Draw(img)
 accent=GENRE_PALETTE[genre]
 d.rounded_rectangle((2,3,width-3,height-4),radius=21,
                     fill=(5,36,50,236),outline=accent,width=3)
 d.rounded_rectangle((13,12,65,height-12),radius=13,fill=accent)
 d.text((39,height/2),step,anchor='mm',fill='#082c38',
        font=ImageFont.truetype(FONT,23))
 d.text((80,height/2),title,anchor='lm',fill='#ffffff',
        font=ImageFont.truetype(FONT,27))
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);img.save(path)
 return str(path)

def render(source,output,png,start=20.9,end=22.5,fade=0.36,
           x=760,y=155,caption_top=1350):
 info=probe(source)
 v=next(s for s in info['streams'] if s['codec_type']=='video')
 a=next((s for s in info['streams'] if s['codec_type']=='audio'),None)
 if a is None: raise ValueError('Existing audio stream required')
 if (v['width'],v['height'])!=(1080,1920): raise ValueError('1080x1920 required')
 im=Image.open(png)
 validate_overlay(x,y,im.width,im.height,v['width'],v['height'],caption_top)
 duration=float(info['format']['duration'])
 if not (0<=start<end<=duration+0.001 and 0<fade<end-start):
  raise ValueError('Invalid timing')
 output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 fg=(f'[1:v]format=rgba,fade=t=in:st={start:.3f}:d={fade:.3f}:alpha=1[card];'
     f'[0:v][card]overlay={x}:{y}:shortest=1:format=auto:'
     f"enable='between(t,{start:.3f},{end:.3f})',format=yuv420p[v]")
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-framerate','30','-loop','1','-i',str(png),'-filter_complex',fg,
      '-map','[v]','-map','0:a:0','-map_metadata','0','-c:v','libx264',
      '-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
      '-c:a','copy','-movflags','+faststart','-t',f'{duration:.3f}',str(output)])
 return {'output':str(output),'genre_count':10,'subtitle_protected':True,
         'japanese_asr_verified':False,'publication_approved':False}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--source',required=True);p.add_argument('--output',required=True)
 p.add_argument('--png',required=True)
 p.add_argument('--genre',default='ai-work',choices=GENRE_PALETTE)
 p.add_argument('--start',type=float,default=20.9)
 p.add_argument('--end',type=float,default=22.5)
 p.add_argument('--fade',type=float,default=0.36)
 args=p.parse_args()
 make_step_card(args.png,genre=args.genre)
 print(json.dumps(render(args.source,args.output,args.png,args.start,args.end,args.fade),ensure_ascii=False))
