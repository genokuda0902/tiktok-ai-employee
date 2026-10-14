"""Cycle569 original offline 2x supersampled illustration. No external images."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import numpy as np
W,H,S=980,955,2
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def font(px,bold=False,mono=False):
    return ImageFont.truetype(MONO if mono else BOLD if bold else REG,px*S)
def xy(box):return tuple(round(v*S) for v in box)
def rr(d,box,r,fill,outline=None,width=1):
    d.rounded_rectangle(xy(box),radius=r*S,fill=fill,outline=outline,width=width*S)
def label(d,x,y,s,px,fill,bold=False,mono=False):
    d.text(xy((x,y)),s,font=font(px,bold,mono),fill=fill)
def smooth(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def render_frame(i,destination):
    assert 0<=i<29
    t=i/28;typing=smooth(t/.31);executing=smooth((t-.31)/.22)
    stage='TYPE' if t<.31 else 'RUN' if t<.53 else 'RESULT'
    yy,xx=np.mgrid[0:H*S,0:W*S].astype(np.float32)
    xx/=W*S;yy/=H*S
    g=np.exp(-((xx-.72)**2/.22+(yy-.38)**2/.14)*2.1)
    g2=np.exp(-((xx-.18)**2/.10+(yy-.72)**2/.25)*1.9)
    grain=np.sin(xx*143+yy*97)*.55
    bg=np.stack([12+15*g+6*g2+grain,23+31*g+17*g2+grain,49+34*g+19*g2+grain],axis=-1)
    im=Image.fromarray(np.uint8(np.clip(bg,0,255)),'RGB').convert('RGBA')
    glow=Image.new('RGBA',im.size,(0,0,0,0));gd=ImageDraw.Draw(glow)
    gd.ellipse(xy((380,205,1120,850)),fill=(38,216,190,36))
    im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(68*S)))
    d=ImageDraw.Draw(im,'RGBA')
    label(d,45,30,'プログラミングを、',39,(221,236,249,255))
    label(d,45,91,'一瞬で体験。',58,(255,255,255,255),bold=True)
    rr(d,(44,187,936,260),21,(20,68,81,245),(92,211,195,190),2)
    label(d,75,200,'1行を書く  →  実行する  →  結果を見る',29,(232,255,250,255),bold=True)
    rr(d,(39,298,940,773),33,(6,17,37,250),(91,162,189,230),2)
    rr(d,(59,321,922,386),17,(22,47,68,255))
    for j,c in enumerate([(251,107,126,255),(252,196,96,255),(78,220,167,255)]):
        d.ellipse(xy((82+26*j,342,97+26*j,357)),fill=c)
    label(d,208,329,'main.py',29,(226,247,253,255),mono=True)
    rr(d,(744,329,885,371),11,(18,94,89,255),(83,212,179,200),2)
    label(d,767,333,'DEMO',23,(224,255,247,255),mono=True)
    label(d,83,417,'CODE',25,(136,191,213,255),mono=True)
    rr(d,(78,464,899,576),20,(13,37,57,255),(62,125,154,230),2)
    command='print("Hello!")';count=round(len(command)*typing)
    code=command[:count]
    label(d,102,478,code,57,(243,248,255,255),mono=True)
    if stage=='TYPE' and i%8<5:
        cur=font(57,mono=True).getlength(code)/S
        rr(d,(105+cur,489,109+cur,556),1,(91,239,202,255))
    for j,(step,word) in enumerate([('01','入力'),('02','実行'),('03','結果')]):
        x=83+j*286
        active=(j==0 and stage=='TYPE') or (j==1 and stage=='RUN') or (j==2 and stage=='RESULT')
        rr(d,(x,601,x+252,659),14,(30,105,100,255) if active else (25,51,72,255),
           (105,247,199,255) if active else (68,117,137,180),2 if active else 1)
        label(d,x+18,611,step,24,(108,233,199,255),mono=True)
        label(d,x+101,608,word,29,(255,255,255,255) if active else (174,211,225,255),bold=True)
    if stage=='RUN':
        label(d,84,690,'RUNNING',25,(135,233,211,255),mono=True)
        rr(d,(250,698,880,717),8,(23,60,75,255))
        rr(d,(250,698,250+round(630*executing),717),8,(82,233,184,255))
    elif stage=='RESULT':
        label(d,84,691,'✓  実行完了',29,(115,240,188,255),bold=True)
    else:label(d,84,692,'入力中…',27,(142,212,227,255),bold=True)
    rr(d,(41,795,938,911),25,(13,58,65,250),(86,192,176,205),2)
    label(d,69,815,'OUTPUT',23,(128,224,212,255),mono=True)
    if stage=='RESULT':
        label(d,343,802,'Hello!',65,(243,255,252,255),bold=True,mono=True)
        d.ellipse(xy((834,832,879,877)),fill=(84,231,171,255))
        d.line([xy((846,854)),xy((858,867)),xy((874,845))],fill=(8,71,55,255),width=5*S)
    else:label(d,352,818,'···',54,(103,171,180,255),mono=True)
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    base=im.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
    extended=Image.new('RGB',(W,1060));extended.paste(base,(0,45))
    extended.paste(base.crop((0,0,W,1)).resize((W,45)),(0,0))
    extended.paste(base.crop((0,H-1,W,H)).resize((W,60)),(0,1000))
    extended.save(destination,optimize=True)
    return {'frame':i,'stage':stage,'characters':count,'result_visible':stage=='RESULT'}
