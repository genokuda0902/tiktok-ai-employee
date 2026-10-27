"""cycle911: platform-UI-safe, high-contrast 3-step final CTA for private review.
No third-party assets, personal data, or fabricated productivity claims.
Usage: python safe_cta.py --out /path/to/frames --genre ai_work
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS = 30
FRAMES = 82
W, H = 1080, 1160
VIDEO_Y = 300
SAFE_RIGHT = 900
SAFE_BOTTOM = 1460
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
PALETTES = {
    'ai_work': ('#19C7B1','#0B77D4'),
    'business': ('#39B5F5','#3477D5'),
    'learning': ('#A68BFF','#7655D8'),
    'health': ('#43D7B2','#1A8C83'),
    'beauty': ('#F19BCB','#C95C96'),
    'travel': ('#58D2E8','#248DAA'),
    'money': ('#7CE0A1','#218C60'),
    'cooking': ('#FFBE78','#C87A3B'),
    'pets': ('#F1CF79','#AD8A32'),
    'entertainment': ('#C9A5FF','#885DC3'),
}
STEPS = [
    ('繰り返す作業を選ぶ', '例：週次報告書の下書き'),
    ('完成形の見本を用意', '欲しい形を先に見せる'),
    ('確認してから保存', '数字・内容・表現をチェック'),
]

def font(sz, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, sz)

def text_bbox(text, size, bold=False):
    return ImageDraw.Draw(Image.new('RGB',(1,1))).textbbox((0,0), text, font=font(size,bold))

def validate_layout():
    assert len(PALETTES) == 10
    assert len(STEPS) == 3
    for title, detail in STEPS:
        assert text_bbox(title,43,True)[2] <= 575, title
        assert text_bbox(detail,30)[2] <= 575, detail
    for box in [(75,40,875,1095),(105,250,845,442),(105,469,845,661),
                (105,688,845,880),(108,934,840,1026)]:
        assert box[2] <= SAFE_RIGHT and box[3]+VIDEO_Y <= SAFE_BOTTOM
    return True

def gradient_background():
    import numpy as np
    yy,xx=np.mgrid[0:H,0:W]
    radial=np.exp(-(((xx-850)/550)**2+((yy-180)/550)**2)*1.5)
    a=np.empty((H,W,3),dtype=np.uint8)
    for i,(dark,light) in enumerate([(6,17),(20,51),(39,81)]):
        a[:,:,i]=np.clip(dark+(light-dark)*radial,0,255)
    return Image.fromarray(a,'RGB').convert('RGBA')

_BASE=None

def base_image():
    global _BASE
    if _BASE is not None: return _BASE
    im=gradient_background()
    shadow=Image.new('RGBA',(W,H),(0,0,0,0))
    sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle((76,48,878,1102),radius=42,fill=(0,0,0,115))
    im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(17)))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((75,40,875,1095),radius=38,fill='#F6F9FF',outline='#C9DDED',width=3)
    d.rounded_rectangle((106,76,358,121),radius=20,fill='#DCECF8')
    d.text((127,81),'今日の1アクション',font=font(24,True),fill='#17516D')
    d.text((109,142),'まずは1つ、試してみよう',font=font(51,True),fill='#102D4B')
    d.text((111,213),'小さな時短を、毎日の習慣に。',font=font(30),fill='#3D5870')
    for i,(title,detail) in enumerate(STEPS):
        top=250+i*219
        d.rounded_rectangle((105,top,845,top+192),radius=27,fill='#FFFFFF',outline='#D5E2EF',width=3)
        d.text((236,top+27),title,font=font(43,True),fill='#12334E')
        d.text((238,top+101),detail,font=font(30),fill='#51677D')
        d.line((235,top+158,797,top+158),fill='#E4EDF5',width=2)
    d.rounded_rectangle((108,934,840,1026),radius=24,fill='#123B59')
    d.text((164,958),'保存前に、人が内容を確認',font=font(34,True),fill='#FFFFFF')
    d.text((125,1052),'架空の説明用画面｜社員確認・手動投稿のみ',font=font(21),fill='#60758B')
    _BASE=im
    return im

def render(frame:int,genre:str='ai_work'):
    if genre not in PALETTES: raise ValueError('Unknown genre')
    if not 0<=frame<FRAMES: raise ValueError('Invalid frame')
    validate_layout()
    primary,secondary=PALETTES[genre]
    im=base_image().copy()
    d=ImageDraw.Draw(im)
    active=min(2,frame//27)
    for i in range(3):
        top=250+i*219
        if i==active:
            d.rounded_rectangle((106,top+1,844,top+191),radius=27,outline=primary,width=7)
            d.rounded_rectangle((808,top+22,820,top+164),radius=6,fill=primary)
        d.ellipse((133,top+45,212,top+124),fill=primary if i==active else '#DDEAF4')
        digit_color='#07263D' if i==active else '#42657E'
        d.text((154,top+51),str(i+1),font=font(44,True),fill=digit_color)
    for i in range(3):
        x=127+i*232
        d.rounded_rectangle((x,906,x+203,916),radius=5,fill=primary if i<=active else '#C8D9E8')
    return im

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    p.add_argument('--genre',default='ai_work')
    args=p.parse_args()
    validate_layout()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    for i in range(FRAMES):render(i,args.genre).save(out/f'{i:03d}.png',compress_level=3)
    print('rendered',FRAMES,'frames to',out)
if __name__=='__main__':main()
