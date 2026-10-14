"""Cycle564: ten-genre review-only CTA frames."""
from dataclasses import dataclass
from PIL import Image,ImageDraw,ImageFont
import math
W,H=720,1280
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
@dataclass(frozen=True)
class Endcard:
 genre:str=GENRES[0]
 headline:str='計算結果は、必ず検算。'
 cta:str='保存して、あとで試そう'
 footer:str='次の時短術もチェック'
 rights:str='original_procedural'
 review_only:bool=True
DEFAULT=Endcard()
def validate(c):
 if c.genre not in GENRES:raise ValueError('genre')
 if c.rights!='original_procedural' or not c.review_only:raise ValueError('approval')
 if any(not s or len(s)>18 or '\n' in s for s in (c.headline,c.cta,c.footer)):raise ValueError('text')
 return True
def smooth(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def frame(c,t,first=None):
 validate(c)
 if not 0<=t<=2:raise ValueError('time')
 im=Image.new('RGB',(W,H),(5,18,35));d=ImageDraw.Draw(im)
 f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',34)
 d.rounded_rectangle((50,185,670,265),radius=25,fill=(13,61,76),outline=(49,204,207),width=3)
 d.text((80,200),'AI時短ラボ',font=f,fill='white')
 d.text((80,370),c.headline,font=f,fill='white')
 d.rounded_rectangle((65,775,655,890),radius=30,fill=(17,121,110),outline=(73,238,214),width=4)
 d.text((90,815),c.cta,font=f,fill='white')
 d.text((100,960),c.footer,font=f,fill='white')
 d.rectangle((80,1060,80+int(560*smooth(t/1.8)),1070),fill=(57,218,204))
 if first is not None and t>=1.66:
  if first.size!=(W,H):raise ValueError('size')
  im=Image.blend(im,first,smooth((t-1.66)/.24))
 return im
