"""Review-only guided focus overlay for synthetic spreadsheet footage.
The full ffmpeg assembly and MP4 QA script is in the downloadable cycle594 package.
"""
import math
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
VALUES=(120,150,200,250)
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
STAGES=(
 {'title':'① 範囲を選ぶ','rect':(386,820,614,1100),'cursor':(605,1089),'label':(644,845)},
 {'title':'② 関数を確認','rect':(294,603,518,675),'cursor':(506,664),'label':(630,609)},
 {'title':'③ 結果を検算','rect':(386,1100,614,1170),'cursor':(606,1160),'label':(642,1111)},
)
def validate(genre,values=VALUES):
 if genre not in GENRES: raise ValueError('unknown genre')
 if len(values)!=4 or any(type(x) is not int or x<0 for x in values): raise ValueError('bad data')
 if sum(values)!=720: raise ValueError('unsupported result')
 for s in STAGES:
  x1,y1,x2,y2=s['rect']
  if not (0<x1<x2<W and 0<y1<y2<H): raise ValueError('unsafe focus rectangle')
 return True
def stage_at(t):
 if not 0<=t<3: raise ValueError('time outside insert')
 return min(2,int(t))
def overlay(im,t):
 s=STAGES[stage_at(t)];d=ImageDraw.Draw(im,'RGBA');x1,y1,x2,y2=s['rect']
 pulse=int(80+60*abs(math.sin(5*t)))
 d.rounded_rectangle((x1-7,y1-7,x2+7,y2+7),radius=11,outline=(11,191,174,pulse),width=8)
 lx,ly=s['label'];font=ImageFont.truetype(FONT,29)
 tw=ImageDraw.Draw(im).textbbox((0,0),s['title'],font=font)[2]
 d.rounded_rectangle((lx-13,ly-10,min(W-70,lx+tw+25),ly+51),radius=14,fill=(10,73,80,230),outline=(52,229,203,255),width=3)
 d.text((lx,ly-2),s['title'],font=font,fill=(255,255,255,255))
 cx,cy=s['cursor'];dx=8*math.sin(6*t);dy=5*math.cos(6*t)
 d.ellipse((cx-17+dx,cy-17+dy,cx+17+dx,cy+17+dy),fill=(255,224,107,215),outline=(15,54,64,255),width=4)
 return im
