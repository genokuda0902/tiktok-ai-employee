"""Review-only, original animated numeric proof trace; no real Excel/ChatGPT recording.
Reimplementation based on synthetic fictional 3-month data; never auto-publish.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,COUNT=1080,1270,30,86
GENRES=('ai_work','money','health','history','science','language','career','lifestyle','travel','education')
PALETTES={
 'ai_work':('#1BDBCF','#F8CC62'), 'money':('#6FE6AA','#F5D47D'),
 'health':('#72D8D2','#F9B9C5'), 'history':('#EFC681','#DFA078'),
 'science':('#77CAFF','#CFA6FF'), 'language':('#A8D9FF','#F8C983'),
 'career':('#73C7FF','#F5C877'), 'lifestyle':('#F3B6D5','#9DE7CB'),
 'travel':('#98D9FC','#FFE19E'), 'education':('#B4C4FF','#FFD18A')}
MONTHS=('4月','5月','6月')
A=(12,16,18)
B=(8,9,12)
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def rgb(s):return tuple(int(s[i:i+2],16) for i in (1,3,5))
def f(size,bold=False):return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)
def totals(a=A,b=B):
    if len(a)!=3 or len(b)!=3:raise ValueError('exactly three months required')
    return sum(a),sum(b)
def stage(frame):
    if not 0<=frame<COUNT:raise ValueError('frame out of range')
    return 0 if frame<23 else 1 if frame<52 else 2

def render_frame(frame,genre='ai_work'):
    if genre not in PALETTES:raise ValueError('unapproved genre')
    s=stage(frame)
    accent,gold=map(rgb,PALETTES[genre])
    im=Image.new('RGB',(W,H),(5,19,34));d=ImageDraw.Draw(im)
    for y in range(H):
        d.line((0,y,W,y),fill=(6+int(8*y/H),21+int(14*y/H),39+int(16*y/H)))
    d.rounded_rectangle((32,29,1048,1210),radius=34,fill=(9,35,53),outline=(58,99,120),width=3)
    d.rounded_rectangle((62,57,1018,151),radius=21,fill=(12,64,80))
    d.ellipse((91,92,114,115),fill=accent)
    d.text((137,74),'SOURCE → FORMULA → RESULT',font=f(31,True),fill=(231,250,252))
    d.text((65,186),'AIの答えは、数字で確かめる',font=f(54,True),fill=(245,250,253))
    d.text((67,272),'架空データで検算の手順を再現',font=f(32),fill=(163,206,222))
    # Spreadsheet mock: the content is explicitly a recreated interface.
    d.rounded_rectangle((65,350,1015,865),radius=25,fill=(240,248,250),outline=accent,width=3)
    d.rounded_rectangle((65,350,1015,419),radius=23,fill=(16,92,81))
    d.text((98,363),'表計算の再現画面',font=f(31,True),fill='white')
    d.text((805,371),'架空の例',font=f(25,True),fill=(240,251,252))
    xs=(110,330,560,795)
    headers=('月','営業A','営業B','確認')
    for j,x in enumerate(xs):d.text((x,446),headers[j],font=f(34,True),fill=(32,59,71))
    for i in range(3):
        top=517+i*96
        active=(s==0 and i==min(2,frame//8)) or (s==1 and i==2) or (s==2 and i==2)
        if active:d.rounded_rectangle((91,top-9,989,top+74),radius=13,fill=(203,244,237))
        for j,val in enumerate((MONTHS[i],str(A[i]),str(B[i]),'✓' if frame>=18+i*2 else '—')):
            d.text((xs[j],top),val,font=f(39,True) if j<3 else f(35),fill=(18,64,78))
        d.line((100,top+79,979,top+79),fill=(183,207,216),width=2)
    d.rounded_rectangle((75,900,1005,1108),radius=23,fill=(12,54,75),outline=(44,101,116),width=2)
    if s==0:
        d.text((100,924),'STEP 1 / 元データを照合',font=f(36,True),fill=accent)
        d.text((100,988),'12・16・18   /   8・9・12',font=f(42,True),fill=(249,253,255))
    elif s==1:
        d.text((100,924),'STEP 2 / 合計式を確認',font=f(36,True),fill=accent)
        d.text((100,986),'=SUM(B2:B4)   →   46',font=f(43,True),fill=(249,253,255))
    else:
        d.text((100,924),'STEP 3 / 2列の結果を比較',font=f(36,True),fill=accent)
        d.text((100,987),'営業A 46   /   営業B 29',font=f(41,True),fill=(249,253,255))
    # Original timeline progress and clear disclosure, outside the subtitle area.
    d.rounded_rectangle((80,1134,998,1145),radius=5,fill=(31,76,91))
    d.rounded_rectangle((80,1134,80+int(918*(frame+1)/COUNT),1145),radius=5,fill=gold)
    d.text((80,1161),'RECREATED UI / FICTIONAL DATA / REVIEW ONLY',font=f(21),fill=(151,195,205))
    return im

def make_frames(folder,genre='ai_work'):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    for i in range(COUNT):render_frame(i,genre).save(folder/f'frame_{i:03d}.png')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--genre',default='ai_work');a=p.parse_args();make_frames(a.out,a.genre)
