"""cycle827: fictional numeric source→output proof, 10-genre overlay, review only.

Uses cycle826's verified H264/AAC renderer and subtitle-safe bounds.
Never represents actual business data, an actual app, or public-release approval.
"""
from __future__ import annotations
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cycle826'))
import interaction826 as prior

GENRES=prior.GENRES
PALETTES=prior.PALETTES
START,END=12.917,16.150
SOURCE=(12,8)
EXPECTED=sum(SOURCE)
DISCLAIMER='架空データの操作イメージ／実在のサービス画面ではありません'

def validate(genre='ai_work',start=START,end=END,source=SOURCE):
    prior.gate(genre,start,end)
    if source!=SOURCE or sum(source)!=EXPECTED or EXPECTED!=20:
        raise ValueError('unverified fictional arithmetic')
    if '架空' not in DISCLAIMER:
        raise ValueError('missing fictional disclaimer')
    return True

def font(size,bold=False):
    return ImageFont.truetype(prior.BOLD_PATH if bold else prior.FONT_PATH,size)

def make_frame(progress,genre='ai_work'):
    validate(genre)
    p=max(0.,min(1.,float(progress)))
    accent=PALETTES[genre]
    W,H=prior.WIDTH,prior.HEIGHT
    im=Image.new('RGB',(W,H),'#102E3D')
    d=ImageDraw.Draw(im)
    # Original layered desk/dashboard visual; no external or private assets.
    d.ellipse((775,-100,1040,160),fill='#305568')
    d.polygon([(0,568),(952,533),(952,648),(0,648)],fill='#343639')
    d.line((0,568,952,533),fill='#927358',width=4)
    d.rounded_rectangle((38,35,915,592),radius=29,fill='#071B27',outline='#587986',width=4)
    d.rounded_rectangle((52,50,901,576),radius=20,fill='#173B4B')
    d.rectangle((52,88,901,132),fill='#244F61')
    for j,c in enumerate(('#FF8981','#EFC86E','#7ED8B4')):
        d.ellipse((79+j*27,103,94+j*27,118),fill=c)
    d.text((171,110),'SOURCE  →  CALCULATE  →  VERIFY',font=font(25,True),fill='white',anchor='lm')
    d.text((878,110),'架空の操作例',font=font(22),fill='#B9DAE2',anchor='rm')
    d.text((82,172),'元データ → 計算 → 確認',font=font(40,True),fill='#F5FAFC')
    d.text((82,222),'AIの回答は、数字を自分で確かめる。',font=font(25),fill='#C3E0E7')
    d.rounded_rectangle((77,264,548,513),radius=14,fill='#F0F7F8')
    d.rounded_rectangle((77,264,548,314),radius=13,fill='#2C687A')
    d.rectangle((77,299,548,314),fill='#2C687A')
    d.text((101,289),'元データ（架空）',font=font(27,True),fill='white',anchor='lm')
    d.text((119,340),'項目',font=font(23,True),fill='#2C4C58')
    d.text((455,340),'件数',font=font(23,True),fill='#2C4C58')
    for i,(name,num) in enumerate(zip(('A','B'),SOURCE)):
        y=372+i*59
        active=(p<.33 and i==0) or (.33<=p<.63 and i==1)
        d.rounded_rectangle((98,y-7,525,y+45),radius=10,fill=accent if active else '#DCECEF')
        d.text((122,y+18),'架空データ '+name,font=font(23,True),fill='#123A49',anchor='lm')
        d.text((458,y+18),str(num),font=font(33,True),fill='#103B4A',anchor='mm')
    d.rounded_rectangle((566,264,878,513),radius=14,fill='#0C3343',outline='#598D9C',width=2)
    d.text((593,293),'数字を検算',font=font(27,True),fill='#D6EAF0',anchor='lm')
    equation=f'{SOURCE[0]} + {SOURCE[1]} = '+('?' if p<.34 else str(EXPECTED))
    d.text((720,363),equation,font=font(33,True),fill='white',anchor='mm')
    d.text((720,433),'?' if p<.34 else str(EXPECTED),font=font(72,True),fill=accent,anchor='mm')
    if p>=.7:
        d.rounded_rectangle((590,467,852,505),radius=14,fill=accent)
        d.text((721,486),'✓ 数字が一致',font=font(24,True),fill='#092E3B',anchor='mm')
    else:
        d.text((721,485),'照合中…',font=font(24),fill='#BCD8E0',anchor='mm')
    for i,label in enumerate(('① 元データ','② 検算','③ 確認')):
        x=85+i*278
        d.rounded_rectangle((x,529,x+253,565),radius=11,fill=accent if p>=i/3 else '#345764')
        d.text((x+126,547),label,font=font(23,True),fill='#102F3A' if p>=i/3 else 'white',anchor='mm')
    d.text((476,617),DISCLAIMER,font=font(18),fill='#C5D5D9',anchor='mm')
    # Subtle motion; the overlay never touches the Japanese subtitle box.
    scale=1+.014*p
    if scale>1:
        w,h=round(W*scale),round(H*scale)
        big=im.resize((w,h),Image.Resampling.BICUBIC)
        l=(w-W)//2;t=(h-H)//2
        im=big.crop((l,t,l+W,t+H))
    return im

def render(source:Path,output:Path,genre='ai_work',start=START,end=END):
    validate(genre,start,end)
    old=prior.make_frame
    prior.make_frame=make_frame
    try:
        result=prior.render(source,output,genre,start,end)
    finally:
        prior.make_frame=old
    result.update({'cycle':827,'prior_cycle':826,'asset_origin':'procedural_original',
        'fictional_math_verified':SOURCE==(12,8) and EXPECTED==20,
        'spoken_japanese_semantics_verified':False,'word_level_subtitle_sync_verified':False,
        'reference_v33_directly_compared':False,'rights_approved_for_publication':False,
        'publication_approved':False,'review_only':True,'auto_post':False})
    return result

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--genre',choices=GENRES,default='ai_work')
    ap.add_argument('--start',type=float,default=START)
    ap.add_argument('--end',type=float,default=END)
    ap.add_argument('--report',type=Path)
    a=ap.parse_args();qa=render(a.source,a.output,a.genre,a.start,a.end)
    if a.report:
        a.report.parent.mkdir(parents=True,exist_ok=True)
        a.report.write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(qa,ensure_ascii=False,indent=2))
    if not all(qa['checks'].values()) or not qa['fictional_math_verified']:
        raise SystemExit('QA FAILED')
