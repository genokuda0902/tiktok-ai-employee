"""Original, rights-safe 3-beat prompt instruction overlay for 10 topic palettes.
Review-only graphic: does not claim actual ChatGPT/Excel app capture.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H=1080,1270
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES=('ai_work','money','health','history','science','language','career','lifestyle','travel','education')
PALETTES={
 'ai_work':('#00DBD3','#FFD25F'), 'money':('#61E6A7','#F5D77E'),
 'health':('#7FE3D4','#F9B9C5'), 'history':('#F3C881','#E7A27B'),
 'science':('#79CFFF','#D1A4FF'), 'language':('#B4DFFF','#FFCF82'),
 'career':('#77C8FF','#F3C97B'), 'lifestyle':('#FFB6D2','#B2E8CA'),
 'travel':('#9EDAFF','#FFE19E'), 'education':('#B5C5FF','#FFD18B'),
}
CARDS=(('01','目的','月別の売上を集計'),('02','条件','架空の4か月分を比較'),('03','形式','表とグラフ用データ'))

def rgb(h):return tuple(int(h[i:i+2],16) for i in (1,3,5))
def font(size,bold=False):return ImageFont.truetype(FONT if bold else FONT_REG,size)
def render_frame(frame:int, genre='ai_work', fps=30)->Image.Image:
    if genre not in PALETTES:raise ValueError('unknown genre')
    if not 0<=frame<87:raise ValueError('frame out of range')
    accent, gold=map(rgb,PALETTES[genre]); t=frame/fps
    im=Image.new('RGBA',(W,H),(5,17,32,255)); d=ImageDraw.Draw(im)
    for y in range(H):
        p=y/H; d.line((0,y,W,y),fill=(6+int(p*7),19+int(p*13),37+int(p*18),255))
    d.rounded_rectangle((35,35,1045,1200),radius=35,fill=(8,30,49),outline=(56,98,122),width=3)
    d.rounded_rectangle((64,64,1016,178),radius=20,fill=(11,52,72))
    d.ellipse((90,105,113,128),fill=accent)
    d.text((131,91),'AI WORKFLOW  /  04',font=font(32,True),fill=(197,239,243))
    d.text((67,212),'AIへの指示は、3つに分ける',font=font(55,True),fill=(248,251,255))
    d.text((70,298),'目的 → 条件 → 出力形式',font=font(37),fill=(162,205,222))
    for i,(num,title,body) in enumerate(CARDS):
        y=378+i*217; active=i==min(2,int(t/.96))
        edge=accent if active else (43,82,102)
        d.rounded_rectangle((66,y,1014,y+194),radius=24,fill=(13,46,66),outline=edge,width=5 if active else 2)
        d.rounded_rectangle((88,y+22,176,y+104),radius=18,fill=(19,89,107) if active else (20,57,76))
        d.text((107,y+33),num,font=font(38,True),fill=accent if active else (124,173,190))
        d.text((205,y+20),title,font=font(40,True),fill=(251,253,255))
        if t>=i*.75:
            d.text((205,y+90),body,font=font(34),fill=(220,238,245))
        else:
            d.rounded_rectangle((206,y+105,780,y+125),radius=8,fill=(41,75,90))
        if active:
            x=88+int(890*min(1,max(0,(t-i*.96)/.95)))
            d.rounded_rectangle((88,y+174,x,y+181),radius=3,fill=gold)
    d.rounded_rectangle((68,1065,1012,1167),radius=22,fill=(16,73,93))
    d.text((100,1083),'例：架空の売上データで説明',font=font(33,True),fill=(239,250,253))
    d.text((70,1182),'RECREATED DEMO / NOT A REAL APP RECORDING',font=font(20),fill=(145,181,194))
    return im

def make_frames(folder:Path, genre='ai_work', count=86):
    folder.mkdir(parents=True,exist_ok=True)
    for i in range(count):render_frame(i,genre).save(folder/f'overlay_{i:03d}.png',optimize=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_work');p.add_argument('--count',type=int,default=86)
    a=p.parse_args();make_frames(Path(a.out),a.genre,a.count)
