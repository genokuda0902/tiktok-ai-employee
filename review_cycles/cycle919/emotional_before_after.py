"""cycle919 original review-only before/after story; no third-party media.

Reimplementation, not the original v33 renderer. Input audio is inherited and NOT
verified by independent Japanese ASR. No posting or external upload.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,START,FRAMES,Y0 = 1080,1290,30,588,103,150
SAFE_CAPTION_Y = 1490
STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work':('AIの下書き','元データで照合','数字は、必ず確かめる'),
 'business':('報告の下書き','実績表で照合','確定値だけを伝える'),
 'learning':('AIの要約','教科書で照合','根拠を確かめて学ぶ'),
 'health':('生活のメモ','記録と照合','観察と判断を分ける'),
 'beauty':('ケアの提案','使用記録と照合','記録をもとに確認する'),
 'travel':('AIの旅程','時刻表と照合','移動条件を確かめる'),
 'money':('支出の集計','元票と照合','金額を確かめて使う'),
 'cooking':('AIのレシピ','分量表と照合','材料と分量を確認する'),
 'pets':('お世話の案','観察記録と照合','記録を見て判断する'),
 'entertainment':('企画の下書き','事実と照合','事実と演出を区別する'),
}
def font(sz,bold=False): return ImageFont.truetype(BOLD if bold else FONT,sz)
def smooth(x):
 x=max(0.,min(1.,x)); return x*x*(3-2*x)
def validate():
 assert len(GENRES)==10
 assert Y0+H < SAFE_CAPTION_Y
 assert START+FRAMES==691
 assert all(len(v)==3 and all(isinstance(t,str) and t for t in v) for v in GENRES.values())
 return True
def gradient(w,h,kind):
 im=Image.new('RGB',(w,h)); pix=im.load()
 for y in range(h):
  yy=y/max(1,h-1)
  for x in range(w):
   xx=x/max(1,w-1)
   spot=max(0.,1.-((xx-.77)**2/.35+(yy-.17)**2/.23))
   if kind=='before': pix[x,y]=(int(41+46*spot+24*yy),int(30+23*spot+12*yy),int(42+27*spot+20*yy))
   else: pix[x,y]=(int(15+22*spot+10*yy),int(54+50*spot+13*yy),int(77+63*spot+18*yy))
 return im
def make_scene(kind, text):
 im=gradient(W,H,kind).convert('RGBA'); d=ImageDraw.Draw(im)
 warm=(255,174,119,130) if kind=='before' else (110,231,242,145)
 b=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(b)
 for x,y,r in [(130,130,70),(870,150,110),(940,570,45),(250,620,45),(760,910,70)]:
  bd.ellipse((x-r,y-r,x+r,y+r),fill=warm)
 im=Image.alpha_composite(im,b.filter(ImageFilter.GaussianBlur(43)));d=ImageDraw.Draw(im)
 d.polygon([(0,800),(W,740),(W,H),(0,H)],fill=(15,27,38,245))
 for x in (65,380,690):
  d.rounded_rectangle((x,165,x+230,620),radius=22,fill=(15,30,45,100),outline=(160,195,220,45),width=3)
 d.polygon([(0,980),(W,920),(W,1080),(0,1130)],fill=(39,49,56,255))
 d.ellipse((95,600,530,1120),fill=(14,25,39,255))
 d.rounded_rectangle((240,580,385,750),radius=32,fill=(172,116,99,255))
 d.ellipse((184,330,443,644),fill=(182,130,111,255))
 d.pieslice((150,284,475,540),185,355,fill=(30,31,42,255))
 d.polygon([(184,455),(160,370),(210,316),(275,280),(365,295),(430,345),(450,460),(417,405),(389,354),(252,365)],fill=(28,29,38,255))
 d.ellipse((256,478,270,488),fill=(35,34,37,255));d.ellipse((354,478,368,488),fill=(35,34,37,255))
 d.arc((282,508,348,560),190 if kind=='before' else 10,350 if kind=='before' else 170,fill=(78,51,48,255),width=5)
 d.rounded_rectangle((465,665,987,994),radius=26,fill=(6,20,32,255),outline=(118,171,193,220),width=7)
 d.rounded_rectangle((488,693,963,947),radius=12,fill=(13,36,49,255))
 d.polygon([(430,997),(1014,997),(1070,1062),(375,1062)],fill=(81,95,103,255))
 if kind=='before':
  for j in range(4):
   x=54+j*65; y=895-j*22
   d.polygon([(x,y),(x+190,y-18),(x+205,y+20),(x+16,y+39)],fill=(236,216,197,255),outline=(165,150,140,255))
  d.text((650,727),'AI DRAFT',font=font(44,True),fill=(255,216,191,255))
  d.text((650,816),'17  ?',font=font(90,True),fill=(255,162,118,255))
  d.line((525,918,900,918),fill=(245,130,102,255),width=6)
 else:
  d.rounded_rectangle((510,710,930,923),radius=18,fill=(227,247,247,255))
  d.text((575,724),'SOURCE CHECK',font=font(37,True),fill=(17,77,90,255))
  d.text((580,805),'18',font=font(87,True),fill=(13,96,106,255))
  d.ellipse((803,803,894,894),fill=(33,173,133,255))
  d.line((822,845,841,865),fill='white',width=10)
  d.line((840,864,874,825),fill='white',width=10)
 return im.convert('RGB')
CACHE={}
def frame(i,genre='ai_work'):
 if not 0<=i<FRAMES:raise ValueError('frame out of range')
 if genre not in GENRES:raise ValueError('unknown genre')
 key=(genre,'before')
 if key not in CACHE:
  a,b,_=GENRES[genre]
  CACHE[key]=make_scene('before',a)
  CACHE[(genre,'after')]=make_scene('after',b)
 before=CACHE[key];after=CACHE[(genre,'after')]
 x=int(W-(W//2)*smooth((i-21)/45))
 out=before.copy()
 if x<W:out.paste(after.crop((x,0,W,H)),(x,0))
 d=ImageDraw.Draw(out)
 d.rectangle((0,0,W,18),fill='#0D3446')
 d.rectangle((0,0,int(W*(i+1)/FRAMES),18),fill='#52D8E8')
 d.rounded_rectangle((35,50,520,205),radius=25,fill='#101925')
 d.text((62,63),'BEFORE',font=font(43,True),fill='#FFBE9C')
 d.text((62,119),'確認前',font=font(56,True),fill='white')
 if x<=800:
  d.rounded_rectangle((550,50,1045,205),radius=25,fill='#0B303C')
  d.text((575,63),'AFTER',font=font(43,True),fill='#83F0DB')
  d.text((575,119),'照合後',font=font(56,True),fill='white')
 d.rounded_rectangle((45,1120,1035,1255),radius=25,fill='#081D2C',outline='#4DA2B4',width=3)
 _,_,tag=GENRES[genre]
 d.text((82,1151),tag,font=font(60,True),fill='#FFFFFF')
 if i>=65:
  d.line((540,300,540,1090),fill='#D8F6F4',width=7)
  d.rounded_rectangle((485,1000,595,1080),radius=35,fill='#1DAF9D')
  d.text((516,1006),'→',font=font(62,True),fill='white')
 d.text((50,1261),'架空の例 / REVIEW ONLY',font=font(21),fill='#D1E8EE')
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--genre',default='ai_work',choices=sorted(GENRES));a=ap.parse_args()
 validate();dst=Path(a.out);dst.mkdir(parents=True,exist_ok=True)
 for i in range(FRAMES):frame(i,a.genre).save(dst/f'{i:03d}.png',compress_level=1)
 print(f'{FRAMES} original frames generated: {dst}')
if __name__=='__main__':main()
