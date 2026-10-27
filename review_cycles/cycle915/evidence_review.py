"""cycle915: original evidence-first review UI slide; 10 genres, no external media.

Renders 87 RGB frames for scene 05 only. These frames are never published;
the surrounding video, original Japanese narration and burned subtitles are
preserved during local review assembly.
"""
from __future__ import annotations
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import argparse, math

W,H,FPS,FRAMES,Y0,START_FRAME=1080,1160,30,87,300,348
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work':('週次報告','売上が大幅に増加した','売上の根拠を確認して記載','#24D0BC'),
 'business':('営業報告','成果が大幅に伸びた','実績の数字を確認して記載','#61BAFF'),
 'learning':('学習記録','必ず成績が上がる','確認できた学習内容を記載','#A89AFF'),
 'health':('生活記録','必ず健康になる','記録できた変化だけを記載','#72DDB4'),
 'beauty':('ケア記録','必ず効果が出る','実際の使用記録だけを記載','#FFAFD1'),
 'travel':('旅行計画','移動は絶対に間に合う','時刻表を確認して記載','#70D7F1'),
 'money':('支出メモ','確実に節約できた','実際の支出額を確認して記載','#7DD8AA'),
 'cooking':('献立メモ','誰でも必ず成功する','手順と分量を確認して記載','#FFC178'),
 'pets':('お世話記録','絶対に安全な方法','確認できたケア内容を記載','#F5D27D'),
 'entertainment':('企画メモ','必ず人気が出る','根拠のある企画内容を記載','#C7A7FF'),
}
STEPS=('数字・根拠','日付・固有名詞','断定的な表現')


def font(n:int,bold:bool=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def measure(text:str,size:int,bold:bool=False):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)))
 box=d.textbbox((0,0),text,font=font(size,bold))
 return box[2]-box[0]
def smooth(t:float):
 t=max(0.,min(1.,t));return t*t*(3-2*t)
def validate():
 assert len(GENRES)==10
 assert Y0+H==1460 and START_FRAME==348 and FRAMES==87
 assert all(measure(t,35,True)<610 for t in STEPS)
 for genre,(topic,bad,good,accent) in GENRES.items():
  assert measure(topic,41,True)<590,genre
  assert measure(bad,39,True)<660,genre
  assert measure(good,36,True)<675,genre
  assert accent.startswith('#') and len(accent)==7
 return True


def base():
 im=Image.new('RGB',(W,H),'#061629')
 d=ImageDraw.Draw(im)
 # Layered cinematic glows, original generated vectors (no photos/assets).
 for r in range(450,35,-12):
  a=int(13*(1-r/480))
  d.ellipse((-200-r//2,-250-r//2,500+r//2,380+r//2),outline=(12+a,35+a,65+a),width=12)
 for x in range(0,W,54):d.line((x,0,x,H),fill='#0A1C30',width=1)
 for y in range(0,H,58):d.line((0,y,W,y),fill='#0A1C30',width=1)
 # App shadow and elevated surface.
 sh=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(sh)
 sd.rounded_rectangle((88,66,903,1100),radius=38,fill=(0,0,0,160))
 im=Image.alpha_composite(im.convert('RGBA'),sh.filter(ImageFilter.GaussianBlur(27)))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((82,60,894,1083),radius=34,fill='#F6F9FC',outline='#D4E4EC',width=3)
 d.rounded_rectangle((82,60,894,178),radius=32,fill='#EAF1F9')
 d.rectangle((82,141,894,178),fill='#EAF1F9')
 for i,c in enumerate(('#FF918B','#FFC66A','#57D5B8')):
  d.ellipse((118+i*33,106,133+i*33,121),fill=c)
 d.text((225,91),'REVIEW WORKSPACE',font=font(27,True),fill='#355A70')
 d.text((118,218),'AIの出力を自分で確認',font=font(46,True),fill='#14334A')
 d.text((120,290),'AIの初稿',font=font(29,True),fill='#426277')
 d.rounded_rectangle((117,338,861,517),radius=24,fill='#FFFFFF',outline='#D6E3EB',width=3)
 d.text((120,562),'確認するポイント',font=font(29,True),fill='#426277')
 for i,s in enumerate(STEPS):
  yy=618+i*70
  d.rounded_rectangle((122,yy,853,yy+58),radius=14,fill='#FFFFFF',outline='#DBE6EE',width=2)
  d.text((188,yy+10),s,font=font(30,True),fill='#2C4B5B')
 d.text((120,862),'修正するなら',font=font(29,True),fill='#426277')
 d.rounded_rectangle((118,910,858,1003),radius=20,fill='#E7F7F3',outline='#B8E6DC',width=3)
 d.text((126,1035),'※架空の画面｜必ず人が確認してから保存',font=font(22),fill='#657F8E')
 return im

_BASE=None

def render(frame:int,genre:str='ai_work'):
 global _BASE
 if not 0<=frame<FRAMES:raise ValueError('frame out of scene')
 if genre not in GENRES:raise ValueError('unknown genre')
 if _BASE is None:_BASE=base()
 topic,bad,good,accent=GENRES[genre]
 im=_BASE.copy();d=ImageDraw.Draw(im)
 stage=min(2,frame//29)
 d.rounded_rectangle((693,216,853,268),radius=16,fill='#14364E')
 d.text((709,225),f'0{stage+1} / 03',font=font(26,True),fill='#FFFFFF')
 d.text((149,356),topic,font=font(29,True),fill='#537286')
 d.text((148,422),bad,font=font(39,True),fill='#1A384A')
 # Show the unsupported claim as the specific item being reviewed.
 d.rounded_rectangle((148,477,373,511),radius=12,fill='#FDE9E9')
 d.text((164,480),'根拠を確認する',font=font(23,True),fill='#B5484D')
 if stage==0:
  p=smooth((frame-3)/19)
  d.rounded_rectangle((131,408,838,474),radius=17,outline='#E56C72',width=5)
  d.line((153,471,153+int(620*p),471),fill='#E56C72',width=7)
 elif stage>=1:
  d.rounded_rectangle((131,408,838,474),radius=17,outline='#E8A0A3',width=3)
  d.line((153,471,773,471),fill='#E9A2A5',width=5)
 # Checklist reveals each row and a moving focus line.
 for i,s in enumerate(STEPS):
  yy=618+i*70
  if stage>=1:
   prog=smooth((frame-29-i*8)/14)
   if prog>0:
    d.rounded_rectangle((142,yy+12,177,yy+47),radius=9,fill=accent)
    d.line((150,yy+29,157,yy+36,169,yy+20),fill='#092F38',width=4)
    d.rounded_rectangle((185,yy+50,185+int(590*prog),yy+54),radius=2,fill=accent)
  else:
   d.ellipse((149,yy+18,169,yy+38),outline='#B9CAD4',width=3)
 # Final correction comes in after the checklist, without asserting a real result.
 if stage==2:
  p=smooth((frame-59)/18)
  d.rounded_rectangle((118,910,858,1003),radius=20,outline=accent,width=4)
  d.rounded_rectangle((141,933,174,968),radius=9,fill=accent)
  d.line((148,950,156,959,167,942),fill='#0D3542',width=4)
  d.text((190,933),good,font=font(36,True),fill='#194B50')
  d.rounded_rectangle((144,1007,144+int(665*p),1014),radius=3,fill=accent)
 else:
  d.text((150,935),'確認した内容だけを残す',font=font(34,True),fill='#66858A')
 # UI stage dots: purposeful progress, not fabricated analytics.
 for i in range(3):
  xx=749+i*31
  d.ellipse((xx,102,xx+13,115),fill=accent if i<=stage else '#9CB4C4')
 return im.convert('RGB')


def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_work');args=p.parse_args()
 validate();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 for i in range(FRAMES):render(i,args.genre).save(out/f'{i:03d}.png')
 print(f'generated {FRAMES} frames for {args.genre}')
if __name__=='__main__':main()
