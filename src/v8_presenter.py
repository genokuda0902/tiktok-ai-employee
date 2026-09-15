#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math
O=Path('assets/robot'); O.mkdir(parents=True,exist_ok=True)
W,H=720,900
# Reusable branded presenter frames. Layered lighting gives depth; no cheap rectangle mascot.
for i in range(12):
 im=Image.new('RGBA',(W,H),(0,0,0,0)); glow=Image.new('RGBA',(W,H),(0,0,0,0)); g=ImageDraw.Draw(glow)
 bob=int(8*math.sin(i/12*math.tau)); cx=360
 g.ellipse((120,80+bob,600,560+bob),fill=(34,211,238,70)); glow=glow.filter(ImageFilter.GaussianBlur(55)); im.alpha_composite(glow); d=ImageDraw.Draw(im)
 # head shell + dark glass face
 d.rounded_rectangle((155,135+bob,565,465+bob),110,fill=(245,250,255,255),outline=(135,220,255,255),width=10)
 d.rounded_rectangle((205,185+bob,515,390+bob),78,fill=(7,18,34,255),outline=(55,145,190,255),width=5)
 # cyan expressive eyes
 wink=i in (4,5)
 d.ellipse((270,255+bob,310,305+bob if not wink else 265+bob),fill=(61,225,255,255))
 d.ellipse((410,255+bob,450,305+bob),fill=(61,225,255,255))
 # neck/body
 d.rounded_rectangle((260,450+bob,460,720+bob),75,fill=(238,246,252,255),outline=(117,205,245,255),width=8)
 d.rounded_rectangle((305,520+bob,415,610+bob),20,fill=(12,35,58,255)); d.text((337,538+bob),'AI',fill=(73,224,255,255))
 # arms: pointing / explaining / CTA variants
 if i<4:
  d.line((270,520+bob,125,390+bob),fill=(240,248,253,255),width=54); d.ellipse((90,345+bob,150,405+bob),fill=(245,250,255,255))
  d.line((450,520+bob,575,590+bob),fill=(240,248,253,255),width=54)
 elif i<8:
  d.line((270,525+bob,135,555+bob),fill=(240,248,253,255),width=54); d.line((450,525+bob,585,555+bob),fill=(240,248,253,255),width=54)
 else:
  d.line((270,520+bob,145,440+bob),fill=(240,248,253,255),width=54); d.line((450,520+bob,575,440+bob),fill=(240,248,253,255),width=54)
 # feet/shadow
 d.ellipse((240,700+bob,340,790+bob),fill=(220,235,245,255)); d.ellipse((380,700+bob,480,790+bob),fill=(220,235,245,255))
 im.save(O/f'presenter_{i:02d}.png')
# canonical presence marker for quality gate
Image.open(O/'presenter_00.png').save(O/'presenter.png')
print('generated',len(list(O.glob('presenter_*.png'))),'presenter frames')
