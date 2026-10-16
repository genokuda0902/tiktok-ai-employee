"""Cycle616 layout constants and original graphics, no downloaded assets."""
from pathlib import Path
from PIL import Image,ImageDraw
W,H=1080,1920
BG_START=1250
CROP=(50,1468,874,1682)
DEST=(50,1275)
SAFE_BOTTOM=1520
def make_plate(path):
    height=H-BG_START
    im=Image.new('RGB',(W,height));p=im.load()
    for y in range(height):
        t=y/(height-1)
        for x in range(W):
            glow=max(0,1-abs(x-540)/650)*max(0,1-t*1.5)
            p[x,y]=(int(2+1.5*glow),int(10+6*glow+2*t),int(21+10*glow+4*t))
    d=ImageDraw.Draw(im,'RGBA')
    d.line([(40,250),(1040,250)],fill=(60,203,195,45),width=2)
    for j in range(6):
        x=75+j*180
        d.line([(x,400),(x+80,400),(x+80,465)],fill=(43,149,155,30),width=2)
    im.save(path)
def make_mask(path):
    w,h=CROP[2]-CROP[0],CROP[3]-CROP[1]
    im=Image.new('L',(w,h),0)
    ImageDraw.Draw(im).rounded_rectangle((2,2,w-3,h-3),radius=14,fill=255)
    im.save(path)
