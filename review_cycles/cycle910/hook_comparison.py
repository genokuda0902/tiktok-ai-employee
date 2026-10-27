"""cycle910: fictional BEFORE/AFTER concept in the first 2.9 seconds.
Offline Pillow RGBA renderer, no personal data, external media, posting or API.
Full private MP4 is generated locally only; never committed to public GitHub.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse

FPS=30; FRAMES=87; WIDTH=952; HEIGHT=1015
PALETTES={
'ai_work':('#0a8fd1','#18b89d'), 'business':('#2777dc','#13a9bc'),
'learning':('#7958df','#12a8ba'), 'health':('#178b78','#3bbf92'),
'beauty':('#ce4a8c','#e19cba'), 'travel':('#147b9d','#32b1df'),
'money':('#22885b','#e1a83a'), 'cooking':('#d57639','#f4a353'),
'pets':('#b68b36','#e3bc5e'), 'entertainment':('#8655c9','#bd82de')}
FREG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FBOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def font(sz,bold=False):return ImageFont.truetype(FBOLD if bold else FREG,sz)
def ease(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def phase(frame,begin,duration):return ease((frame/FPS-begin)/duration)
def text_width(text,size,bold=False):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)))
 b=d.textbbox((0,0),text,font=font(size,bold));return b[2]-b[0]
def validate_layout():
 assert len(PALETTES)==10
 for s in ('毎回ゼロから','まず1つを型にする','実績ではなく説明用イメージ'):
  assert text_width(s,42,True)<850
 return True
def draw_overlay(frame,genre='ai_work'):
 if genre not in PALETTES:raise ValueError('unknown genre')
 if frame<0 or frame>=FRAMES:raise ValueError('frame range')
 primary,accent=PALETTES[genre]
 im=Image.new('RGBA',(WIDTH,HEIGHT),(0,0,0,0))
 shadow=Image.new('RGBA',(WIDTH,HEIGHT),(0,0,0,0));sd=ImageDraw.Draw(shadow)
 sd.rounded_rectangle((18,22,934,995),radius=35,fill=(0,0,0,90))
 shadow=shadow.filter(ImageFilter.GaussianBlur(13));im.alpha_composite(shadow)
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((12,9,940,986),radius=33,fill='#f4f8ff',outline='#e0ebf6',width=3)
 d.rounded_rectangle((42,34,910,144),radius=25,fill='#e5f1fb')
 d.text((69,50),'毎回ゼロから？',font=font(55,True),fill='#153552')
 bx=(42,181,453,772);ax=(499,181,910,772)
 d.rounded_rectangle(bx,radius=28,fill='#fff1f2',outline='#f1c8d0',width=3)
 d.rounded_rectangle(ax,radius=28,fill='#e9f9f5',outline='#a6ddd1',width=3)
 d.rounded_rectangle((65,207,259,268),radius=18,fill='#b74156')
 d.text((86,215),'BEFORE',font=font(30,True),fill='white')
 d.rounded_rectangle((522,207,697,268),radius=18,fill=accent)
 d.text((547,215),'AFTER',font=font(30,True),fill='white')
 d.text((66,303),'毎回ゼロから',font=font(40,True),fill='#63303d')
 d.text((522,303),'まず1つを型にする',font=font(35,True),fill='#15594e')
 d.text((68,359),'作業の流れが決まらない',font=font(23),fill='#8b4e5c')
 d.text((523,359),'手順を決めて迷いを減らす',font=font(23),fill='#37776b')
 before=('何から始める？','毎回考え直す','確認が後回し')
 after=('作業を1つ選ぶ','見本を用意する','最後に確認する')
 for j in range(3):
  y=426+j*103
  d.rounded_rectangle((66,y,428,y+78),radius=16,fill='white')
  d.rounded_rectangle((523,y,886,y+78),radius=16,fill='white')
  d.ellipse((81,y+20,119,y+58),fill='#edcbd2')
  d.text((88,y+19),'×',font=font(25,True),fill='#aa4558')
  d.text((132,y+20),before[j],font=font(27,True),fill='#663d49')
  d.ellipse((539,y+20,577,y+58),fill=accent)
  d.text((547,y+20),'✓',font=font(25,True),fill='white')
  d.text((591,y+20),after[j],font=font(27,True),fill='#174b45')
 stage=min(2,int((frame/FPS)/0.96))
 p=phase(frame,stage*0.96,0.35)
 y=426+stage*103
 d.rounded_rectangle((521,y-2,889,y+80),radius=17,outline=accent,width=3+round(3*p))
 d.rounded_rectangle((45,806,906,908),radius=22,fill='#153d60')
 d.text((75,820),'作業を整理 → 見本 → 確認',font=font(39,True),fill='white')
 d.rounded_rectangle((66,930,885,942),radius=6,fill='#cfdfed')
 d.rounded_rectangle((66,930,66+int(819*(frame+1)/FRAMES),942),radius=6,fill=accent)
 d.text((70,951),'実績ではなく説明用イメージ｜人による確認が必要',font=font(18),fill='#57718a')
 return im
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_work')
 a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 validate_layout()
 for i in range(FRAMES):draw_overlay(i,a.genre).save(out/f'{i:03d}.png',compress_level=1)
 print('rendered',FRAMES)
if __name__=='__main__':main()
