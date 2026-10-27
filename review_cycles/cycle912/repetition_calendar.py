"""cycle912: evidence-led repetition calendar slide; review-only, no external media.
Frames replace only visual area y=300..1459 of scene 02 in a private MP4.
No personal data, no productivity promises, no automatic posting.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,FRAMES=1080,1160,30,87
Y_OFFSET=300
SAFE_RIGHT=900
SAFE_BOTTOM=1460
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES={
 'ai_work':('#24D4C4','週次報告','週次報告の下書き'),
 'business':('#56B8FF','定例報告','定例報告の下書き'),
 'learning':('#B69BFF','復習記録','復習記録の整理'),
 'health':('#62D5AF','生活記録','生活記録の整理'),
 'beauty':('#FF9ACB','ケア記録','ケア記録の整理'),
 'travel':('#61D6F0','旅程確認','旅程の下書き'),
 'money':('#80D9A2','支出記録','支出記録の整理'),
 'cooking':('#FFC178','献立作成','献立の下書き'),
 'pets':('#F5D27D','お世話記録','お世話記録の整理'),
 'entertainment':('#C8A7FF','企画メモ','企画メモの整理'),
}
DAYS=('第1週','第2週','第3週')
OTHER=('返信を確認','資料を整理','進捗を確認')

def f(size:int,bold:bool=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)

def fit(text:str,size:int,maxw:int,bold:bool=False)->bool:
    return ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0),text,font=f(size,bold))[2]<=maxw

def validate():
    assert len(GENRES)==10
    assert Y_OFFSET+H==SAFE_BOTTOM
    assert 88+3*252-18 <= SAFE_RIGHT
    for accent,task,detail in GENRES.values():
        assert fit(task,36,185,True),(task,'task')
        assert fit(detail,42,690,True),(detail,'detail')
    assert fit('毎週、同じ作業がある',48,790,True)
    assert fit('3週間並べると、繰り返しが見える',30,790)
    return True

def ease(t):
    t=max(0,min(1,t));return 1-(1-t)**3

def rgb(hexcolor):
    return tuple(int(hexcolor[i:i+2],16) for i in (1,3,5))

def bg():
    yy,xx=np.mgrid[0:H,0:W]
    halo=np.exp(-((xx-360)**2/(580**2)+(yy-340)**2/(520**2))*1.8)
    arr=np.zeros((H,W,3),np.uint8)
    for c,(lo,hi) in enumerate(((6,17),(17,48),(35,82))):
        arr[:,:,c]=np.clip(lo+(hi-lo)*halo,0,255)
    im=Image.fromarray(arr,'RGB').convert('RGBA')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((47,36,894,1106),radius=38,fill=(13,36,64,245),outline=(66,113,146,180),width=3)
    d.rounded_rectangle((79,70,322,118),radius=21,fill=(32,83,105,255))
    d.text((102,79),'WORKFLOW / 03',font=f(24,True),fill='#C5FAF5')
    d.text((79,154),'毎週、同じ作業がある',font=f(48,True),fill='white')
    d.text((81,231),'3週間並べると、繰り返しが見える',font=f(30),fill='#BCD2E5')
    for i,day in enumerate(DAYS):
        x=88+i*252
        d.rounded_rectangle((x,332,x+232,764),radius=27,fill=(237,246,253,255),outline=(164,202,220,255),width=3)
        d.rounded_rectangle((x+14,348,x+218,410),radius=18,fill='#E2ECF6')
        d.text((x+26,359),day,font=f(31,True),fill='#153B58')
        d.rounded_rectangle((x+20,670,x+212,726),radius=14,fill='#E9F0F7')
        d.text((x+30,684),OTHER[i],font=f(25),fill='#61778D')
    d.text((91,796),'共通する作業を見つける',font=f(30,True),fill='#D6E8F2')
    d.rounded_rectangle((79,844,884,1046),radius=29,fill='#EDF7FF')
    d.text((107,866),'最初に仕組み化するなら',font=f(28),fill='#37647D')
    d.text((90,1072),'※架空の例｜実行前に人が内容を確認',font=f(22),fill='#8EABC0')
    return im

BASE=None
def render(idx:int,genre='ai_work'):
    if genre not in GENRES:raise ValueError('unknown genre')
    if not 0<=idx<FRAMES:raise ValueError('bad frame')
    global BASE
    if BASE is None:BASE=bg()
    accent,task,detail=GENRES[genre]
    im=BASE.copy();d=ImageDraw.Draw(im)
    for i in range(3):
        start=i*17
        opacity=ease((idx-start)/12)
        if opacity<=0:continue
        x=88+i*252
        lift=round((1-opacity)*24)
        y=448+lift
        d.rounded_rectangle((x+19,y,x+213,y+153),radius=20,fill='#FFFFFF',outline=accent,width=5)
        d.rounded_rectangle((x+30,y+16,x+111,y+50),radius=13,fill=accent)
        d.text((x+44,y+19),'毎週',font=f(19,True),fill='#09273B')
        d.text((x+31,y+65),task,font=f(36,True),fill='#13344F')
        d.text((x+32,y+115),'繰り返し',font=f(22),fill='#58748C')
        if idx-start<16:
            d.arc((x+4,y-15,x+229,y+170),start=210,end=210+int(280*opacity),fill=accent,width=5)
    for i in range(2):
        t=ease((idx-(i+1)*17)/10)
        if t<=0:continue
        x1=88+i*252+214;x2=88+(i+1)*252+19
        d.line((x1,526,x1+(x2-x1)*t,526),fill=accent,width=7)
    t=ease((idx-55)/20)
    if t>0:
        d.rounded_rectangle((104,921,104+round(748*t),1018),radius=19,fill=accent)
        if t>0.55:
            d.text((128,939),detail,font=f(42,True),fill='#072B3E')
    for i in range(3):
        cx=792+i*28
        d.ellipse((cx,90,cx+12,102),fill=accent if idx>=i*17 else '#4C7085')
    return im.convert('RGB')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    p.add_argument('--genre',default='ai_work')
    args=p.parse_args()
    validate()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    for i in range(FRAMES):
        render(i,args.genre).save(out/f'{i:03d}.png',compress_level=3)
    print('OK',FRAMES,args.genre)

if __name__=='__main__':main()
