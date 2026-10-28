"""cycle918: Original task-to-focus hook illustration for 10 genres.

Review-only: creates frames, never posts, uploads or handles personal data.
Only replace source video frames 0..86, pixels y=300..1459; existing
burned Japanese captions and AAC voice are kept from an inherited source.
"""
from __future__ import annotations
import argparse, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,N,FPS,TOP=1080,1160,87,30,300
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work':('仕事を速くする最初の一歩',('週次報告','資料整理','メール作成'),'まず１つ選ぶ','#54E5C5'),
 'business':('成果につなげる最初の一歩',('商談記録','顧客対応','提案準備'),'まず１つ選ぶ','#69C8FF'),
 'learning':('学習を続ける最初の一歩',('単語復習','問題演習','要点整理'),'まず１つ選ぶ','#AFA4FF'),
 'health':('記録を続ける最初の一歩',('睡眠記録','運動記録','食事記録'),'まず１つ選ぶ','#79DDB9'),
 'beauty':('ケアを整える最初の一歩',('朝のケア','夜のケア','使用記録'),'まず１つ選ぶ','#FFB8D1'),
 'travel':('旅を組み立てる最初の一歩',('移動予定','持ち物','立寄り先'),'まず１つ選ぶ','#80D9F1'),
 'money':('家計を整える最初の一歩',('食費','固定費','日用品'),'まず１つ選ぶ','#A2E4AB'),
 'cooking':('料理を楽にする最初の一歩',('献立','買い物','下ごしらえ'),'まず１つ選ぶ','#FFD18A'),
 'pets':('お世話を整える最初の一歩',('食事','散歩','体調記録'),'まず１つ選ぶ','#E9D48A'),
 'entertainment':('企画を形にする最初の一歩',('アイデア','構成','台本'),'まず１つ選ぶ','#C7ABFF'),
}
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else REG,size)
def smooth(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def textwidth(s,size,bold=False):
 f=font(size,bold);return ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),s,font=f)[2]
def validate():
 assert (W,H,N,FPS,TOP)==(1080,1160,87,30,300)
 assert len(GENRES)==10
 for k,(title,tasks,action,accent) in GENRES.items():
  assert len(tasks)==3 and len(set(tasks))==3,k
  assert textwidth(title,49,True)<970,k
  assert all(textwidth(x,42,True)<260 for x in tasks),k
  assert textwidth(action,77,True)<800,k
  assert accent.startswith('#') and len(accent)==7,k
 return True
_BASE=None
def background():
 yy,xx=np.mgrid[0:H,0:W];u=xx/W;v=yy/H
 g1=np.exp(-(((u-.1)/.38)**2+((v-.13)/.28)**2)*2)
 g2=np.exp(-(((u-.88)/.36)**2+((v-.84)/.31)**2)*2)
 out=np.empty((H,W,3),dtype=np.uint8)
 out[:,:,0]=np.clip(8+17*v+12*g1+24*g2,0,255)
 out[:,:,1]=np.clip(23+22*v+43*g1+20*g2,0,255)
 out[:,:,2]=np.clip(46+24*v+48*g1+18*g2,0,255)
 im=Image.fromarray(out,'RGB');d=ImageDraw.Draw(im)
 for i in range(-H,W,110):d.line((i,0,i+H,H),fill='#1D3954',width=2)
 for x,y,r in [(120,105,15),(890,280,12),(940,990,16),(150,940,9)]:
  d.ellipse((x-r,y-r,x+r,y+r),outline='#2E6070',width=3)
 return im
def center_text(d,xy,s,size,fill,bold=True):
 x,y=xy;d.text((x,y),s,font=font(size,bold),anchor='mm',fill=fill)
def paper_card(im,cx,cy,label,accent,scale=1,opacity=1,angle=0,selected=False):
 cw,ch=int(295*scale),int(355*scale)
 if cw<20:return
 layer=Image.new('RGBA',(cw+80,ch+80),(0,0,0,0));d=ImageDraw.Draw(layer)
 d.rounded_rectangle((45,49,cw+39,ch+43),radius=int(30*scale),fill=(0,0,0,85))
 d.rounded_rectangle((40,40,cw+35,ch+35),radius=int(29*scale),fill='#F2F7FA',outline=accent if selected else '#AEC7D4',width=max(2,int(6*scale)))
 d.rounded_rectangle((65,65,cw+10,104),radius=12,fill=accent if selected else '#C9DDE6')
 d.rounded_rectangle((68,135,cw+8,143),radius=3,fill='#C5D5DE')
 d.rounded_rectangle((68,161,cw-33,169),radius=3,fill='#D8E4EA')
 d.rounded_rectangle((68,187,cw-6,195),radius=3,fill='#D8E4EA')
 center_text(d,((cw+80)//2,int(ch*.67)),label,int(39*scale),'#17374C',True)
 if selected:
  d.ellipse((cw-30,94,cw+14,138),fill=accent)
  d.line((cw-19,114,cw-10,122,cw+4,104),fill='#103747',width=max(2,int(5*scale)))
 if angle:layer=layer.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 if opacity<1:
  a=layer.getchannel('A').point(lambda p:int(p*opacity));layer.putalpha(a)
 im.paste(layer,(int(cx-layer.width/2),int(cy-layer.height/2)),layer)
def render(i,genre='ai_work'):
 global _BASE
 if not 0<=i<N:raise ValueError('frame out of range')
 if genre not in GENRES:raise ValueError('unsupported genre')
 if _BASE is None:_BASE=background()
 title,tasks,action,accent=GENRES[genre]
 im=_BASE.copy();d=ImageDraw.Draw(im)
 d.rounded_rectangle((55,47,1025,173),radius=28,fill='#102E48',outline='#3E6880',width=3)
 center_text(d,(540,108),title,49,'#FFFFFF')
 d.text((65,200),'3 TASKS',font=font(24,True),fill='#9AC4D5')
 d.text((815,200),'FOCUS / 01',font=font(24,True),fill=accent)
 if i<29:
  p=smooth(i/28)
  for j,(cx,cy,rot) in enumerate(((230,514,-8),(540,490,0),(850,514,8))):
   paper_card(im,cx,cy+int((1-p)*65),tasks[j],accent,scale=.87,angle=rot,opacity=.8+.2*p)
  d=ImageDraw.Draw(im)
  center_text(d,(540,890),'やることが多いときは',51,'#D7E9F1')
  center_text(d,(540,972),'最初の１つを決める',61,accent)
 elif i<58:
  p=smooth((i-29)/28)
  paper_card(im,220-int(120*p),500,tasks[0],accent,scale=.8-.15*p,angle=-8,opacity=1-.7*p)
  paper_card(im,860+int(120*p),500,tasks[2],accent,scale=.8-.15*p,angle=8,opacity=1-.7*p)
  paper_card(im,540,500-int(25*p),tasks[1],accent,scale=.95+.14*p,selected=True)
  d=ImageDraw.Draw(im)
  center_text(d,(540,906),'まず、対象をしぼる',61,'#FFFFFF')
  d.rounded_rectangle((275,957,805,972),radius=7,fill='#294D5F')
  d.rounded_rectangle((275,957,275+int(530*p),972),radius=7,fill=accent)
 else:
  p=smooth((i-58)/28)
  d=ImageDraw.Draw(im)
  d.ellipse((205,250,875,920),outline='#2B6572',width=5)
  d.ellipse((270,316,810,856),outline='#28617A',width=2)
  d.rounded_rectangle((145,348,935,786),radius=48,fill='#F1F7FA',outline=accent,width=9)
  d.rounded_rectangle((193,390,887,473),radius=25,fill='#D7EBEF')
  center_text(d,(540,433),'FOCUS 01',39,'#29566D')
  center_text(d,(540,578),tasks[1],82,'#183C50')
  d.ellipse((487,674,593,780),fill=accent)
  d.line((511,724,535,749,569,704),fill='#173C4D',width=12)
  center_text(d,(540,915+int((1-p)*35)),action,77,'#FFFFFF')
  d.rounded_rectangle((265,1004,815,1020),radius=8,fill='#2C5161')
  d.rounded_rectangle((265,1004,265+int(550*p),1020),radius=8,fill=accent)
 d=ImageDraw.Draw(im)
 d.text((64,1102),'ORIGINAL ART  •  HUMAN REVIEW ONLY',font=font(22),fill='#92B7C6')
 return im
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--genre',default='ai_work');ap.add_argument('--sample',action='store_true');args=ap.parse_args()
 validate();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 ids=(0,43,86) if args.sample else range(N)
 for i in ids:render(i,args.genre).save(out/f'{i:03d}.png',compress_level=2)
 print('rendered',len(ids),'frames',args.genre)
if __name__=='__main__':main()
