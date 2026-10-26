"""Original rights-safe illustrated closer; 10 genre layouts, review-only MP4.

No robot animation or third-party assets. Static illustration with gentle camera
movement and text reveal; original private AAC and burned captions are retained.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,FRAMES,START,COUNT=1080,1358,30,691,588,103
CAPTION_Y=1490
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
'ai_work':('小さな時短を','今日から1つ'),
'sales_business':('今日の営業を','一歩改善する'),
'beauty':('今日のケアを','一つ続ける'),
'romance':('今日の会話を','少し大切に'),
'saving':('今日の支出を','一つ見直す'),
'career':('今日の学びを','一つ実践する'),
'wellness':('今日の習慣を','一つ整える'),
'science':('今日の疑問を','一つ調べる'),
'travel_food':('次のお出かけを','一つ計画する'),
'product_comparison_lifestyle':('今日の選択を','一つ見直す'),
}
POLICY={'review_only':True,'publication_approved':False,'automatic_posting':False,
'external_upload':False,'source_rights_reviewed':False,'original_procedural_art':True}

@lru_cache(maxsize=20)
def font(size):return ImageFont.truetype(FONT,size)
def ease(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def radial(size,cx,cy,rgb,base=(4,15,30),sx=330,sy=460):
 w,h=size;y,x=np.ogrid[:h,:w]
 glow=np.exp(-(((x-cx)/sx)**2+((y-cy)/sy)**2)*1.5)[...,None]
 out=np.clip(np.asarray(base)[None,None,:]+glow*np.asarray(rgb)[None,None,:],0,255).astype('uint8')
 return Image.fromarray(out,'RGB')

def glossy_robot():
 """Painted from primitive gradients, not an external photo, logo or likeness."""
 im=radial((W,H),735,420,(25,89,139),sx=500,sy=680).convert('RGBA')
 d=ImageDraw.Draw(im,'RGBA')
 # Soft depth-of-field light points; deterministic, no random external assets.
 bokeh=Image.new('RGBA',(W,H));b=ImageDraw.Draw(bokeh,'RGBA')
 for j in range(55):
  x=(j*173+51)%W;y=(j*269+97)%1010;r=5+(j*7)%27
  b.ellipse((x-r,y-r,x+r,y+r),fill=(81,196,253,20+(j%4)*8))
 bokeh=bokeh.filter(ImageFilter.GaussianBlur(15))
 im=Image.alpha_composite(im,bokeh);d=ImageDraw.Draw(im,'RGBA')
 # Floating particles and perspective floor.
 d.polygon([(0,1080),(1080,1005),(1080,1358),(0,1358)],fill=(7,20,35,230))
 for j in range(7):
  y=1120+j*35;d.line((0,y,1080,y-55),fill=(50,117,153,24),width=2)
 # Main backlight and soft shadow.
 glow=Image.new('RGBA',(W,H));g=ImageDraw.Draw(glow,'RGBA')
 g.ellipse((175,245,970,1150),fill=(19,180,255,92))
 im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(105)))
 d=ImageDraw.Draw(im,'RGBA')
 d.ellipse((270,1090,875,1225),fill=(0,0,0,140))
 # Shoulders, chest, silver metal layers.
 d.rounded_rectangle((290,760,865,1120),radius=170,fill=(151,194,211,255),outline=(222,249,255,255),width=11)
 d.rounded_rectangle((324,795,825,1110),radius=155,fill=(230,244,246,255))
 d.rounded_rectangle((425,854,730,1030),radius=65,fill=(18,45,68,255),outline=(106,211,236,255),width=10)
 d.rounded_rectangle((468,902,689,976),radius=30,fill=(14,88,126,255))
 d.text((501,908),'AI',font=font(45),fill=(199,249,255,255))
 # Ears and neck joints.
 d.rounded_rectangle((214,430,312,655),radius=42,fill=(154,205,225,255),outline=(237,252,255,255),width=8)
 d.rounded_rectangle((801,430,901,655),radius=42,fill=(154,205,225,255),outline=(237,252,255,255),width=8)
 d.rounded_rectangle((472,728,649,834),radius=35,fill=(69,118,151,255))
 # Head chrome outer case, inner glass and reflections.
 d.rounded_rectangle((260,270,854,770),radius=175,fill=(201,233,245,255),outline=(244,254,255,255),width=15)
 d.rounded_rectangle((288,300,825,741),radius=155,fill=(238,248,249,255))
 d.rounded_rectangle((324,344,789,688),radius=115,fill=(7,24,44,255),outline=(89,169,202,255),width=11)
 d.arc((355,365,759,690),185,340,fill=(58,128,165,100),width=8)
 # High contrast emissive eyes with layered bloom.
 eye=Image.new('RGBA',(W,H));e=ImageDraw.Draw(eye,'RGBA')
 for x in (451,661):
  e.ellipse((x-68,448,x+68,583),fill=(17,181,255,210))
 eye=eye.filter(ImageFilter.GaussianBlur(24));im=Image.alpha_composite(im,eye)
 d=ImageDraw.Draw(im,'RGBA')
 for x in (451,661):
  d.ellipse((x-48,464,x+48,566),fill=(25,203,255,255))
  d.ellipse((x-29,475,x+27,543),fill=(121,244,255,255))
  d.ellipse((x-26,475,x-3,496),fill=(239,255,255,240))
 d.arc((483,543,632,620),15,165,fill=(82,221,247,245),width=9)
 # Chrome highlights and contour detail.
 d.arc((278,285,830,750),185,315,fill=(255,255,255,170),width=12)
 d.arc((316,348,794,695),200,310,fill=(119,215,240,70),width=5)
 d.ellipse((745,373,766,395),fill=(170,246,255,150))
 # Glassy lower-left lens flare.
 flare=Image.new('RGBA',(W,H));f=ImageDraw.Draw(flare,'RGBA')
 f.ellipse((105,670,465,1010),fill=(0,185,255,30))
 im=Image.alpha_composite(im,flare.filter(ImageFilter.GaussianBlur(60)))
 return im.convert('RGB')

@lru_cache(maxsize=1)
def base_art():return glossy_robot()

def text_fits(d,text,xy,size,max_x):
 if d.textbbox(xy,text,font=font(size))[2]>max_x:raise ValueError('text clipped: '+text)

def draw_frame(i,genre='ai_work'):
 if genre not in GENRES:raise ValueError('unknown genre')
 if not 0<=i<COUNT:raise ValueError('frame out of range')
 # Small camera motion on a single static original illustration; no robot motion.
 art=base_art();z=1+0.020*ease(i/(COUNT-1))
 nw,nh=round(W*z),round(H*z)
 if z>1:art=art.resize((nw,nh),Image.Resampling.BICUBIC).crop(((nw-W)//2,(nh-H)//2,(nw+W)//2,(nh+H)//2))
 im=art.convert('RGBA');overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay,'RGBA')
 d.rounded_rectangle((60,42,1020,244),radius=30,fill=(5,20,37,224),outline=(90,200,236,115),width=3)
 first,second=GENRES[genre]
 text_fits(d,first,(101,66),57,980)
 d.text((101,66),first,font=font(57),fill=(235,249,255,255))
 if i>=12:
  text_fits(d,second,(101,135),68,980)
  d.text((101,135),second,font=font(68),fill=(97,233,255,255))
 if i>=48:
  d.rounded_rectangle((83,1114,998,1226),radius=38,fill=(0,104,192,232),outline=(174,241,255,245),width=4)
  cta='保存して、明日1つ試す'
  text_fits(d,cta,(139,1138),48,975)
  d.text((139,1138),cta,font=font(48),fill=(255,255,255,255))
  d.ellipse((925,1142,973,1190),fill=(61,231,230,255))
  d.line((936,1166,947,1177,965,1156),fill=(3,45,75,255),width=6)
 if i>=80:
  d.text((307,1267),'※ 公開前に人が確認',font=font(28),fill=(175,212,231,255))
 im=Image.alpha_composite(im,overlay)
 return im.convert('RGB')

def media_info(p):
 obj=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)],text=True))
 v=next(x for x in obj['streams'] if x['codec_type']=='video')
 a=next(x for x in obj['streams'] if x['codec_type']=='audio')
 if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']),a['codec_name'],a['sample_rate'])!=('h264',1080,1920,'30/1',691,'aac','48000'):raise ValueError('wrong source or output AV')

def render(source,output,manifest,genre='ai_work'):
 source,output=Path(source),Path(output)
 if genre not in GENRES or not source.is_file() or source.resolve()==output.resolve() or output.exists():raise ValueError('unsafe paths/genre')
 if manifest!={**POLICY,'source_sha256':sha(source)}:raise ValueError('source rights manifest rejected')
 media_info(source)
 with tempfile.TemporaryDirectory(prefix='cycle868_') as tmp:
  tmp=Path(tmp)
  # Avoid new assets/voices; overlay original illustration above existing captions.
  for i in range(COUNT):draw_frame(i,genre).save(tmp/f'{i:03d}.jpg',quality=91,subsampling=0)
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
        f'[0:v][new]overlay=x=0:y=132:enable=\'between(n,{START},{START+COUNT-1})\':'
        'eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),'-framerate','30','-start_number','0','-i',str(tmp/'%03d.jpg'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
  subprocess.run(cmd,check=True,timeout=240)
 media_info(output)
 return {'input_sha256':sha(source),'output_sha256':sha(output),'changed_frames':COUNT,'frame_range':[START,START+COUNT-1],'genre':genre,'genres_supported':len(GENRES),'policy':POLICY}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--manifest',required=True);p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');a=p.parse_args()
 r=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
 Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(r,ensure_ascii=False))
