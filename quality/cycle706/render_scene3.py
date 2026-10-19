"""Cycle706 original scene-3 illustration; 60 frames at 30 fps, no external assets.
Raspberry Pi connection *schematic*, not a product photo.
Usage: python quality/cycle706/render_scene3.py /tmp/frames science
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, sys

FPS,N=30,60
COLORS={
 "science":(71,224,208),"ai_work":(66,228,215),"beauty":(255,146,201),
 "love_psychology":(255,179,212),"saving":(134,231,169),
 "sales_business":(101,208,249),"career":(169,189,255),
 "health":(128,231,193),"travel_food":(255,196,119),
 "product_comparison":(196,172,255)}
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def font(n,bold=False): return ImageFont.truetype(BOLD if bold else FONT,n)
def mix(a,b,p): return tuple(round(x*(1-p)+y*p) for x,y in zip(a,b))
def ease(p): p=max(0,min(1,p));return p*p*(3-2*p)
def cable(d,points,p,color):
    lens=[math.dist(a,b) for a,b in zip(points,points[1:])]
    rem=sum(lens)*ease(p)
    for a,b,l in zip(points,points[1:],lens):
        q=min(1,rem/l)
        end=(round(a[0]+(b[0]-a[0])*q),round(a[1]+(b[1]-a[1])*q))
        if q>0:
            d.line((a,end),fill=color,width=5,joint="curve")
            d.ellipse((end[0]-5,end[1]-5,end[0]+5,end[1]+5),fill=color)
        rem-=min(l,rem)
        if rem<=0:break
def frame(i,genre="science"):
    if genre not in COLORS or not 0<=i<N:raise ValueError("bad genre/frame")
    c=COLORS[genre];t=i/FPS;W,H=736,604
    im=Image.new("RGB",(W,H));d=ImageDraw.Draw(im)
    for y in range(H):
        p=y/H;d.line((0,y,W,y),fill=(round(3+3*p),round(22+7*p),round(37+8*p)))
    d.rounded_rectangle((2,2,W-3,H-3),radius=31,outline=c,width=3)
    for x in range(40,W,45):d.line((x,105,x,H-24),fill=(8,39,53))
    for y in range(115,H-20,45):d.line((24,y,W-24,y),fill=(8,39,53))
    d.rounded_rectangle((26,22,221,61),radius=16,fill=(8,48,60),outline=c,width=2)
    d.text((42,25),"CONNECTION  /  03",font=font(22,True),fill=(217,243,243))
    d.text((30,72),"画面と入力機器をつなぐ",font=font(34,True),fill=(245,251,251))
    d.rounded_rectangle((42,200,297,393),radius=21,fill=(11,65,64),outline=c,width=3)
    d.rounded_rectangle((67,229,270,363),radius=12,fill=(11,92,78),outline=(41,177,145),width=2)
    for x in range(82,267,29):
        for y in (245,351):d.ellipse((x-3,y-3,x+3,y+3),fill=(224,187,101))
    d.rounded_rectangle((135,270,213,328),radius=7,fill=(10,30,43),outline=(118,202,205),width=2)
    d.text((154,280),"CPU",font=font(20,True),fill=(226,250,248))
    for yy,col in ((249,(223,193,112)),(325,(180,197,206))):
        d.rounded_rectangle((270,yy,306,yy+36),radius=4,fill=(27,51,57),outline=col,width=2)
    d.text((64,402),"小型コンピューター基板",font=font(20,True),fill=(216,242,240))
    hdmi=[(304,267),(351,267),(351,247),(394,247)]
    usb=[(304,343),(338,343),(338,463),(408,463)]
    for path in (hdmi,usb):d.line(path,fill=(37,78,87),width=9,joint="curve")
    cable(d,hdmi,(t-.10)/.63,c);cable(d,usb,(t-.78)/.60,(255,193,104))
    on=ease((t-.65)/.25)
    d.rounded_rectangle((397,168,696,370),radius=21,fill=(9,34,48),outline=mix((54,111,125),c,on*.78),width=4)
    d.rounded_rectangle((414,185,678,348),radius=11,fill=mix((4,16,28),(4,47,56),on),outline=(30,91,101),width=2)
    for j,col in enumerate(((236,111,114),(239,188,92),(81,200,179))):
        d.ellipse((432+25*j,200,443+25*j,211),fill=col)
    if t>.72:
        d.text((431,229),"> python3 app.py",font=font(20),fill=(200,237,235))
        if t>1.28:d.text((431,263),"接続を確認中...",font=font(22),fill=c)
        if t>1.64:
            d.rounded_rectangle((428,298,659,338),radius=10,fill=(11,81,73))
            d.text((443,301),"✓ 操作の準備OK",font=font(23,True),fill=(244,254,252))
    d.polygon([(519,371),(572,371),(582,406),(509,406)],fill=(33,104,113))
    d.rounded_rectangle((481,404,610,416),radius=5,fill=(72,156,163))
    d.text((451,137),"画面  /  HDMI",font=font(21,True),fill=(220,244,243))
    active=ease((t-1.18)/.28)
    d.rounded_rectangle((413,446,658,510),radius=12,fill=mix((12,32,45),(17,66,75),active),outline=(255,193,104),width=3)
    for r in range(3):
        for col in range(11):
            x=427+col*19;y=458+r*13
            d.rounded_rectangle((x,y,x+14,y+9),radius=2,fill=mix((34,61,69),(78,157,152),active))
    d.ellipse((667,449,709,505),fill=(17,58,66),outline=(103,171,168),width=3)
    d.text((428,516),"入力  /  USB",font=font(21,True),fill=(228,243,237))
    for j,(txt,when) in enumerate((("① 画面",.72),("② 入力",1.4),("③ 操作",1.7))):
        x=37+j*231;on=t>=when
        d.rounded_rectangle((x,556,x+214,587),radius=12,fill=(14,70,69) if on else (9,40,54),outline=c if on else (38,83,91),width=2)
        d.text((x+15,557),txt,font=font(19,True),fill=(238,255,251) if on else (126,173,180))
    return im
def full_frame(i,genre="science"):
    c=COLORS[genre];W,H=870,792
    im=Image.new("RGB",(W,H));d=ImageDraw.Draw(im)
    for y in range(H):
        p=y/H;d.line((0,y,W,y),fill=(round(3+3*p),round(19+8*p),round(35+8*p)))
    d.rounded_rectangle((2,2,W-3,H-3),radius=37,outline=c,width=4)
    d.text((70,28),"03  /  CONNECTION STORY",font=font(24,True),fill=(159,221,218))
    im.paste(frame(i,genre),(67,90))
    ImageDraw.Draw(im).text((88,719),"HDMI で画面、USB で入力機器を接続",font=font(24,True),fill=(210,238,236))
    return im
def generate(outdir,genre="science"):
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    for i in range(N):full_frame(i,genre).save(out/f"frame_{i:03d}.png",optimize=True)
if __name__=="__main__":
    generate(sys.argv[1] if len(sys.argv)>1 else "frames",sys.argv[2] if len(sys.argv)>2 else "science")
