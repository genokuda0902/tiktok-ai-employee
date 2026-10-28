"""cycle921: original three-beat saved-prompt walkthrough for 10 genres.
No external media, real account UI, performance claims or publication controls.
Rendered at 540x580 then Lanczos upscaled to 1080x1160; replace scene 07 only.
"""
from __future__ import annotations
import argparse, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W,H,N,FIRST=540,580,87,522
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
PRESETS={
 'ai_work':('AI仕事術','週次報告テンプレート','仕事の型','次回も使える形で保存'),
 'business':('ビジネス','提案書テンプレート','営業資料','次回も使える形で保存'),
 'learning':('学習','復習メモの型','学習メモ','内容を見直して保存'),
 'health':('健康記録','体調記録の型','健康メモ','内容を見直して保存'),
 'beauty':('美容','ケア記録の型','美容メモ','内容を見直して保存'),
 'travel':('旅行','旅程メモの型','旅行計画','日程を確認して保存'),
 'money':('家計','支出記録の型','家計メモ','金額を確認して保存'),
 'cooking':('料理','献立メモの型','レシピ','材料を確認して保存'),
 'pets':('ペット','お世話記録の型','お世話メモ','内容を確認して保存'),
 'entertainment':('エンタメ','企画メモの型','企画資料','内容を確認して保存'),
}
def f(s,bold=False):return ImageFont.truetype(BOLD if bold else REG,s)
def ease(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)
def width(text,size,bold=False):return ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),text,font=f(size,bold))[2]
def validate_presets():
 assert len(PRESETS)==10
 for key,vals in PRESETS.items():
  assert len(vals)==4 and all(vals)
  assert width(vals[1],25,True)<370,key
  assert width(vals[2],20,True)<210,key
  assert width(vals[3],19,True)<370,key
 return True
def gradient():
 yy,xx=np.mgrid[0:H,0:W];x=xx/W;y=yy/H
 glow=np.exp(-(((x-.77)/.58)**2+((y-.12)/.48)**2)*2.4)
 a=np.empty((H,W,3),dtype=np.uint8)
 for i,(base,v,light) in enumerate([(7,7,17),(18,13,24),(35,19,36)]):a[:,:,i]=np.clip(base+v*y+light*glow,0,255)
 return Image.fromarray(a)
def rr(d,xy,r,fill,outline=None,width=1):d.rounded_rectangle(tuple(map(int,xy)),radius=r,fill=fill,outline=outline,width=width)
def txt(d,xy,s,size,fill,bold=False):d.text(xy,s,font=f(size,bold),fill=fill)
def shadow_panel(im,rect,fill='#F7FAFE'):
 sh=Image.new('RGBA',im.size,(0,0,0,0));sd=ImageDraw.Draw(sh)
 x1,y1,x2,y2=rect;rr(sd,(x1+4,y1+8,x2+4,y2+8),16,(0,0,0,130))
 sh=sh.filter(ImageFilter.GaussianBlur(12));im.paste(sh,(0,0),sh)
 rr(ImageDraw.Draw(im),rect,16,fill,'#D7E5F4',1)
def draw(index,genre='ai_work'):
 if genre not in PRESETS:raise ValueError('genre')
 if not 0<=index<N:raise ValueError('frame')
 cat,doc,folder,verify=PRESETS[genre]
 t=index/86;beat=min(2,int(index/29));phase=(index%29)/28
 im=gradient();d=ImageDraw.Draw(im)
 for x in range(-400,600,54):d.line((x,0,x+320,580),fill='#15334D',width=1)
 rr(d,(22,20,518,562),24,'#10273D','#3A5A72',2)
 rr(d,(40,35,165,62),12,'#1D4562')
 txt(d,(54,42),'WORKFLOW / 07',11,'#B9EAF0',True)
 txt(d,(403,42),'SAVE GUIDE',10,'#86B5C8',True)
 txt(d,(43,82),'使える指示を保存する',29,'#FFFFFF',True)
 txt(d,(44,126),'名前 → 保存先 → 確認',16,'#B7D3E6')
 for k,label in enumerate(['1 名前','2 保存先','3 確認']):
  left=44+k*155
  rr(d,(left,166,left+143,202),11,'#0E6C94' if k==beat else '#263F57')
  txt(d,(left+21,174),label,15,'#FFFFFF' if k==beat else '#A8C1D1',True)
 shadow_panel(im,(42,225,499,493));d=ImageDraw.Draw(im)
 rr(d,(42,225,499,267),15,'#E5EDF7')
 rr(d,(42,247,499,268),0,'#E5EDF7')
 for i,c in enumerate(['#FF8983','#FFCE75','#73D5B1']):d.ellipse((58+i*19,240,69+i*19,251),fill=c)
 txt(d,(354,238),'LOCAL EXAMPLE',10,'#657C90',True)
 rr(d,(59,280,164,471),12,'#E8F0F8')
 for k,lb in enumerate(['すべて','仕事の型','保存済み']):
  y=296+k*54
  if k==(1 if beat>=1 else 0):rr(d,(68,y-6,156,y+35),9,'#C9E9F6')
  txt(d,(79,y),lb,13,'#174D66' if k==(1 if beat>=1 else 0) else '#6B8295',k==(1 if beat>=1 else 0))
 rr(d,(177,279,482,468),12,'#FFFFFF','#D5E1EC',1)
 rr(d,(191,295,229,337),9,'#DDF4F4')
 txt(d,(202,301),'文',19,'#177A8C',True)
 txt(d,(241,298),'テンプレート',14,'#687E8E',True)
 txt(d,(192,349),doc,24,'#182F48',True)
 d.line((193,390,463,390),fill='#DDE7F1',width=2)
 txt(d,(193,403),['名前をつける','保存先を選ぶ','内容を確認する'][beat],18,'#175E86',True)
 if beat==0:
  xx=194+int(250*ease(phase));d.line((194,441,xx,441),fill='#1B8AC6',width=7)
  if phase>.34:txt(d,(425,415),'✓',21,'#179A89',True)
 elif beat==1:
  s=1+0.07*math.sin(phase*math.pi)
  x,y=407,428
  rr(d,(x-27*s,y-10*s,x+27*s,y+20*s),5,'#0E9CC3')
  rr(d,(x-24*s,y-19*s,x+5*s,y-5*s),3,'#2CC8DF')
  txt(d,(192,429),folder,16,'#1C6B81',True)
 else:
  rr(d,(194,424,463,454),8,'#E3F8EF')
  txt(d,(202,427),'✓ '+verify,14,'#14755E',True)
 rr(d,(42,510,499,550),11,'#163A54')
 msg=['名前をつけて探しやすく','フォルダで整理する','保存後に内容を見直す'][beat]
 txt(d,(63,519),msg,17,'#E8F8FD',True)
 return im.resize((1080,1160),Image.Resampling.LANCZOS)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_work');p.add_argument('--preview-only',action='store_true');a=p.parse_args()
 validate_presets();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 indices=[9,40,73] if a.preview_only else range(N)
 for i in indices:draw(i,a.genre).save(out/f'frame_{FIRST+i:04d}.png',compress_level=2)
 print('generated',len(indices),'frames')
if __name__=='__main__':main()
