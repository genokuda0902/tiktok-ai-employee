"""Original synthetic, high-contrast, result-first visual for 1080x1920."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W,H=1080,1920
VALUES=(120,150,200,250)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def font(size):return ImageFont.truetype(FONT,size)
def center(draw,text,y,size,color):
    f=font(size);box=draw.textbbox((0,0),text,font=f)
    draw.text(((W-box[2]+box[0])/2,y),text,font=f,fill=color)
def make_background():
    y,x=np.mgrid[0:H,0:W]
    halo=np.exp(-(((x-540)/1080)**2/.12+((y-730)/1920)**2/.13))
    a=np.empty((H,W,3),dtype=np.uint8)
    a[:,:,0]=np.clip(7+8*halo,0,255)
    a[:,:,1]=np.clip(18+35*halo,0,255)
    a[:,:,2]=np.clip(37+80*halo,0,255)
    return Image.fromarray(a,'RGB')
def make_frame(t,bg):
    im=bg.copy();d=ImageDraw.Draw(im)
    d.rounded_rectangle((68,170,1012,258),radius=23,fill='#12364a',outline='#39d6df',width=2)
    center(d,'AI時短ラボ | 検証デモ',185,42,'white')
    center(d,'その合計、まだ手計算？',332,76,'white')
    center(d,'4か月の売上を、一目で検算',452,47,'#8ae2ed')
    d.rounded_rectangle((138,560,942,952),radius=70,fill='#0b3344',outline='#40e9e4',width=5)
    center(d,'検算した合計',603,52,'white')
    q=min(1.0,max(0,t/.65))
    center(d,str(round(720*(1-(1-q)**3))),625,194,'white')
    center(d,'※架空のサンプルデータ',895,29,'#99b7c7')
    center(d,'入力値を確かめる',1030,50,'white')
    for i,v in enumerate(VALUES):
        x=75+i*240
        d.rounded_rectangle((x,1140,x+210,1290),radius=27,fill='#144558',outline='#39d6df',width=3)
        d.text((x+36,1150),str(i+1)+'月',font=font(34),fill='white')
        d.text((x+38,1203),str(v),font=font(62),fill='white')
    if t>=.7:
        d.rounded_rectangle((100,1340,980,1460),radius=26,fill='#0b6760',outline='#36dcbf',width=3)
        center(d,'120 + 150 + 200 + 250 = 720',1363,45,'white')
    d.rounded_rectangle((50,1625,1030,1775),radius=18,fill='#0c3446',outline='#3d93a6',width=2)
    center(d,'検証手順 01/08 | 結果を先に表示',1641,35,'#a6e8f3')
    center(d,'架空データ：4か月の売上合計は720',1700,43,'white')
    center(d,'再現映像／音声はBGMのみ／要確認',1805,24,'#9cb2c0')
    return im
