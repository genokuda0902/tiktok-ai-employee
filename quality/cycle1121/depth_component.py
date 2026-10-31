"""Offline original layered-workstation component for 10 genre slide templates.

No third-party media, no claims of actual automation or time savings.
Visual-only, requires human review; this module does not post or publish.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math

GENRES=("ai_work","business","money","learning","health","lifestyle","psychology","science","history","travel")
ACCENTS=("#58E5D8","#71B8FF","#F6CA76","#A4A1FF","#6FE5B4","#F5A5BF","#CE9CF6","#8FDDFB","#E4BA8C","#81D8D3")
W,H=951,803
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def smooth(v):
    v=max(0.,min(1.,v))
    return v*v*(3-2*v)
def label(d,xy,s,size,color):
    f=ImageFont.truetype(FONT,size) if Path(FONT).exists() else ImageFont.load_default()
    d.text(xy,s,font=f,fill=color)
def rr(d,rect,r,fill,outline=None,width=1):
    d.rounded_rectangle(rect,radius=r,fill=fill,outline=outline,width=width)

def draw_depth_hero(t,genre="ai_work"):
    """Generate one original perspective-laptop story illustration (951x803)."""
    if genre not in GENRES: raise ValueError("unsupported genre")
    accent=rgb(ACCENTS[GENRES.index(genre)])
    hero=Image.new("RGBA",(W,H),(8,28,46,255))
    glow=Image.new("RGBA",(W,H))
    gd=ImageDraw.Draw(glow)
    gd.ellipse((215,40,900,740),fill=(*accent,65))
    hero=Image.alpha_composite(hero,glow.filter(ImageFilter.GaussianBlur(95)))
    d=ImageDraw.Draw(hero)
    rr(d,(1,1,W-2,H-2),32,None,(43,91,108),3)
    rr(d,(28,24,378,87),19,(23,62,79),(55,109,120),2)
    label(d,(49,36),"毎週の同じ作業",30,accent)
    for i,(day,task) in enumerate((("月","週次報告"),("火","週次報告"),("水","週次報告"))):
        if smooth((t-.12-i*.24)/.68)==0: continue
        x=int(40+15*i+16*math.sin(t*2+i))
        y=int(160+i*132-15*smooth((t-.12-i*.24)/.68))
        rr(d,(x+13,y+15,x+403,y+130),21,(2,13,26))
        rr(d,(x,y,x+390,y+115),21,(24,58,74),accent,3)
        rr(d,(x+18,y+19,x+88,y+91),16,(41,94,103))
        label(d,(x+33,y+32),day,33,accent)
        label(d,(x+116,y+32),task,34,(245,251,254))
    d.ellipse((422,654,933,746),fill=(3,15,27))
    screen=((492,194),(862,143),(892,596),(506,636))
    d.polygon(((480,205),(870,152),(906,608),(498,653)),fill=(4,13,25))
    d.line((*screen,screen[0]),fill=accent,width=7)
    d.polygon(((515,222),(845,179),(871,566),(528,600)),fill=(10,42,63))
    label(d,(547,262),"作業を見つける",33,"white")
    for i,s in enumerate(("同じ報告","同じ入力","同じ確認")):
        yy=338+i*75
        rr(d,(550,yy,828,yy+60),12,(23,72,86))
        rr(d,(564,yy+16,592,yy+43),7,accent if i==0 else (48,102,117))
        label(d,(606,yy+13),s,25,"white")
    d.polygon(((504,644),(903,599),(939,676),(563,736),(418,683)),fill=(31,61,79))
    d.polygon(((512,654),(895,613),(908,644),(561,711),(458,681)),fill=(58,93,108))
    for i in range(5):
        yy=662+i*8
        d.line((548+i*4,yy,859+i*2,yy-38),fill=(20,49,66),width=3)
    if smooth((t-.65)/.95)>0:
        d.line((405,460,476,460,493,411),fill=accent,width=8)
        d.polygon(((493,411),(472,428),(498,434)),fill=accent)
    rr(d,(35,738,916,787),15,(17,51,67))
    label(d,(59,746),"まずは繰り返し作業を「書き出す」",28,(230,248,250))
    return hero.convert("RGB")
