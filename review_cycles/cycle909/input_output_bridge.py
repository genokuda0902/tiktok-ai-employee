"""Cycle909: offline, rights-safe fictional input-to-output visual bridge.
No posting, no external API, no personal data, no actual claims.
Overlay replaces only scene04 demo panel; subtitles and audio remain inherited.
"""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFont

W,H=952,1195
BASE_W=816
PANEL_H=890
FPS=30
FRAMES=87
PALETTES={
 'ai_work':('#0075d5','#17b5a4'), 'business':('#2563eb','#0ea5e9'),
 'learning':('#7c3aed','#06b6d4'), 'health':('#08916a','#34b399'),
 'beauty':('#db2777','#f472b6'), 'travel':('#0e7490','#38bdf8'),
 'money':('#15803d','#eab308'), 'cooking':('#c2410c','#fb923c'),
 'pets':('#a16207','#f59e0b'), 'entertainment':('#9333ea','#f472b6')
}
LABELS=('目的','条件','形式')
INPUTS=('週次報告を作る','数字と根拠を入れる','箇条書き3点')
OUTPUTS=('今週の成果','改善ポイント','次の行動')
DISCLAIMER='架空のデモ｜出力内容は必ず人が確認'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def font(sz,bold=False): return ImageFont.truetype(BOLD if bold else FONT,sz)
def ease(x):
 x=max(0.,min(1.,x))
 return x*x*(3-2*x)
def interp(t,start,duration): return ease((t-start)/duration)
def rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def mix(a,b,p):
 a=rgb(a) if isinstance(a,str) else a
 b=rgb(b) if isinstance(b,str) else b
 return tuple(round(x+(y-x)*p) for x,y in zip(a,b))
def rect(d,xy,fill,r=16,outline=None,width=1):
 d.rounded_rectangle(tuple(int(v) for v in xy),radius=r,fill=fill,outline=outline,width=width)
def centered(d,xy,text,f,fill):
 box=d.textbbox((0,0),text,font=f)
 d.text((xy[0]-(box[2]-box[0])/2,xy[1]-(box[3]-box[1])/2),text,font=f,fill=fill)
def text_fits(text,size,max_width):
 d=ImageDraw.Draw(Image.new('RGB',(1,1)))
 return d.textbbox((0,0),text,font=font(size))[2] <= max_width

def render_frame(i,genre='ai_work'):
 if genre not in PALETTES: raise ValueError('unsupported genre')
 if not 0<=i<FRAMES: raise ValueError('frame out of bounds')
 primary,accent=PALETTES[genre]
 t=i/FPS
 im=Image.new('RGB',(BASE_W,PANEL_H),'#f4f8ff')
 d=ImageDraw.Draw(im)
 rect(d,(0,0,BASE_W-1,PANEL_H-1),'#f4f8ff',30)
 rect(d,(28,26,788,126),'#e5f1ff',22)
 d.text((50,46),'指示から成果物へ',font=font(42,True),fill='#123252')
 rect(d,(592,51,760,103),primary,18)
 centered(d,(676,78),'AI WORKFLOW',font(20,True),'white')
 d.text((40,148),'3つの条件が、見やすい報告に変わる',font=font(27),fill='#46617f')
 rect(d,(32,215,353,697),'white',24,outline='#cbdbea',width=3)
 rect(d,(54,235,164,282),primary,15)
 centered(d,(109,259),'INPUT',font(24,True),'white')
 d.text((58,306),'伝える内容',font=font(30,True),fill='#183858')
 for j,(label,value) in enumerate(zip(LABELS,INPUTS)):
  p=interp(t,0.12+j*0.27,0.34)
  if p<=0: continue
  y=365+j*98
  x=57+int((1-p)*26)
  rect(d,(x,y,x+270,y+81),mix('#eef5fd','#e7fbf7',p),16,outline=mix('#dbe6f1',accent,p),width=2)
  d.text((x+15,y+10),label,font=font(21,True),fill=primary)
  d.text((x+15,y+39),value,font=font(23,True),fill='#20384f')
 phase=interp(t,0.85,0.45)
 line_color=mix('#bfd0e1',accent,phase)
 d.line([(370,449),(436,449)],fill=line_color,width=10)
 d.polygon([(429,430),(452,449),(429,468)],fill=line_color)
 rect(d,(374,372,448,418),mix('#e9f0f8',accent,phase),16)
 centered(d,(411,395),'AI',font(27,True),'white' if phase>.35 else '#627b96')
 if phase>.1:
  cx=376+int(57*((t*1.8)%1))
  d.ellipse((cx-7,442,cx+7,456),fill='#ffffff',outline=accent,width=3)
 p=interp(t,1.35,0.52)
 rect(d,(466,215,782,697),mix('#f4f8ff','#ffffff',p),24,outline=mix('#d6e1ee',accent,p),width=3)
 rect(d,(489,235,627,282),accent if p>.4 else '#b3c6d7',15)
 centered(d,(558,259),'OUTPUT',font(24,True),'white')
 d.text((491,306),'週次報告書',font=font(30,True),fill='#183858')
 for j,value in enumerate(OUTPUTS):
  q=interp(t,1.62+j*0.26,0.3)
  if q<=0: continue
  y=363+j*100
  rect(d,(489,y,758,y+82),'#f0f6fc',15,outline='#d3e2ef',width=2)
  rect(d,(503,y+16,542,y+57),accent,12)
  centered(d,(522,y+37),str(j+1),font(22,True),'white')
  d.text((552,y+21),value,font=font(24,True),fill='#20384f')
 rect(d,(32,729,783,814),'#dfeefa',20)
 d.text((53,744),'架空の例：実績・自動投稿ではありません',font=font(25,True),fill='#214260')
 d.text((53,782),'人による確認・承認後に手動投稿',font=font(18),fill='#48647f')
 d.line([(50,843),(765,843)],fill='#c9d9e9',width=9)
 d.line([(50,843),(50+int(715*(i+1)/FRAMES),843)],fill=accent,width=9)
 outer=Image.new('RGB',(W,PANEL_H),'#f4f8ff')
 outer.paste(im,((W-BASE_W)//2,0))
 rect(ImageDraw.Draw(outer),(0,0,W-1,PANEL_H-1),None,30,outline='#d9e5f4',width=3)
 full=Image.new('RGB',(W,H),'#06142e')
 ImageDraw.Draw(full).text((12,17),'目的と条件を具体的に',font=font(49,True),fill='white')
 full.paste(outer,(0,95))
 d2=ImageDraw.Draw(full)
 rect(d2,(0,970,W-1,H-1),'#f4f8ff',26,outline='#d9e5f4',width=3)
 rect(d2,(45,1005,907,1140),'#dceefc',20)
 rect(d2,(68,1034,124,1090),accent,17)
 centered(d2,(96,1062),'✓',font(31,True),'white')
 d2.text((145,1018),'出力は必ず確認する',font=font(37,True),fill='#183858')
 d2.text((145,1076),'内容を確認し、必要なら修正して保存',font=font(23),fill='#45617c')
 return full

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_work')
 a=p.parse_args();path=Path(a.out);path.mkdir(parents=True,exist_ok=True)
 for i in range(FRAMES): render_frame(i,a.genre).save(path/f'{i:03d}.png',compress_level=1)
 print('rendered',FRAMES,'frames',path)
if __name__=='__main__': main()
