"""cycle914: original illustrated paper/report photo-slide, no external assets.

The rendered image occupies video rows 300..1459 only. It deliberately does not
alter narration, burned captions, original header, or publication controls.
"""
from __future__ import annotations
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from pathlib import Path
import argparse, math

W,H,FPS,FRAMES,Y0=1080,1160,30,87,300
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work': ('週次報告','今週の成果','気づき','次の行動','#25CDB8'),
 'business': ('営業報告','活動内容','改善点','次の行動','#56B8FF'),
 'learning': ('学習記録','学んだこと','気づき','次の学習','#A89AFF'),
 'health': ('生活記録','生活の振り返り','気づき','次の習慣','#69D6AA'),
 'beauty': ('ケア記録','今週のケア','気づき','次のケア','#FFA4CC'),
 'travel': ('旅行計画','行きたい場所','確認事項','次の準備','#70D7F1'),
 'money': ('支出メモ','今週の支出','気づき','次の確認','#7DD8AA'),
 'cooking': ('献立メモ','作る料理','必要な材料','次の準備','#FFC178'),
 'pets': ('お世話記録','今週の様子','気づき','次のお世話','#F5D27D'),
 'entertainment': ('企画メモ','企画の内容','気づき','次の制作','#C7A7FF'),
}
TEXTS=('内容を3つに整理','数字・根拠を確認','担当と期限を決める')

def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
def fit(t,n,max_width,b=False):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)))
 return d.textbbox((0,0),t,font=font(n,b))[2]<=max_width

def validate():
 assert len(GENRES)==10
 assert Y0+H==1460
 assert 895<900
 for genre, (title,*rest) in GENRES.items():
  assert fit(title,62,600,True),(genre,title)
  for txt in rest[:-1]:assert fit(txt,39,460,True),(genre,txt)
 assert all(fit(t,26,520) for t in TEXTS)
 return True

def bg():
 rng=np.random.default_rng(914)
 y,x=np.mgrid[0:H,0:W]
 base=30+20*np.exp(-((x-230)**2/600**2+(y-180)**2/600**2))
 grain=(np.sin(y/4.2+x/95)*2.2+np.sin(y/14+x/180)*2.5+rng.normal(0,1.8,(H,W)))
 glow=np.exp(-((x-260)**2/(520**2)+(y-70)**2/(580**2)))
 a=np.empty((H,W,3),np.uint8)
 for c,mult in enumerate((1.1,.83,.67)):
  a[:,:,c]=np.clip((base+grain)*mult+glow*(18 if c==0 else 10),0,255)
 im=Image.fromarray(a,'RGB').convert('RGBA')
 sh=Image.new('RGBA',(W,H));ds=ImageDraw.Draw(sh)
 ds.rounded_rectangle((79,61,899,1120),radius=30,fill=(0,0,0,185))
 im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(36)))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((77,55,891,1105),radius=27,fill='#F8F7F2',outline='#C9C7BC',width=3)
 for yy in range(130,1060,5):
  if yy%15==0:d.line((106,yy,859,yy),fill='#F2F1EB',width=1)
 d.rounded_rectangle((113,104,323,151),radius=14,fill='#E2F2EF')
 d.text((131,111),'SAMPLE / REPORT',font=font(23,True),fill='#246D65')
 d.line((120,283,848,283),fill='#D5D6D1',width=3)
 d.text((126,318),'完成形の見本',font=font(38,True),fill='#263C45')
 d.text((128,370),'「何を書くか」が一目で分かる形に',font=font(25),fill='#6C7B80')
 for i in range(3):
  yy=437+i*184
  d.rounded_rectangle((122,yy,849,yy+154),radius=22,fill='#FFFFFF',outline='#E2E6E4',width=3)
  d.rounded_rectangle((143,yy+24,191,yy+72),radius=15,fill='#E8F0EE')
  d.text((158,yy+31),str(i+1),font=font(27,True),fill='#526E70')
  d.line((225,yy+105,815,yy+105),fill='#E4E8E6',width=2)
  d.line((225,yy+127,725,yy+127),fill='#EDF0EE',width=2)
 d.text((126,1053),'※架空の見本｜内容と数字は必ず人が確認',font=font(22),fill='#697A7C')
 return im

_BG=None
def render(frame:int,genre:str='ai_work'):
 global _BG
 if genre not in GENRES:raise ValueError('unknown genre')
 if not 0<=frame<FRAMES:raise ValueError('frame outside scene')
 if _BG is None:_BG=bg()
 title,*others=GENRES[genre]
 accent=others[-1];labels=others[:-1]
 im=_BG.copy();d=ImageDraw.Draw(im)
 d.text((126,177),title,font=font(62,True),fill='#152F3A')
 d.text((129,250),'WEEKLY / DRAFT',font=font(23,True),fill='#7B898B')
 for i,label in enumerate(labels):
  yy=437+i*184
  d.text((220,yy+27),label,font=font(39,True),fill='#1B3946')
  d.text((225,yy+76),TEXTS[i],font=font(26),fill='#657A81')
  t=max(0,min(1,(frame-i*25)/15))
  if t>0:
   x1=220;x2=x1+int(570*t)
   d.rounded_rectangle((x1,yy+112,x2,yy+120),radius=4,fill=accent)
   if frame<i*25+22:
    d.rounded_rectangle((119,yy-3,852,yy+157),radius=24,outline=accent,width=5)
 stage=min(2,frame//29)
 for i in range(3):
  cx=752+i*31
  d.ellipse((cx,112,cx+14,126),fill=accent if i<=stage else '#D3DCDA')
 return im.convert('RGB')

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_work');args=p.parse_args()
 validate();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 for i in range(FRAMES):render(i,args.genre).save(out/f'{i:03d}.png',optimize=False)
 print(f'generated {FRAMES} original frames in {out}')
if __name__=='__main__':main()
