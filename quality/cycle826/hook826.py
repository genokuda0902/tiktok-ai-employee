"""Reusable, fully original mobile-readable BEFORE/AFTER hook panel.
No unverified time-savings claim, personal data, brand UI, or publishing calls.
"""
from PIL import Image, ImageDraw, ImageFont

FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def apply_hook(panel: Image.Image, accent: str) -> Image.Image:
    if panel.size != (780, 460):
        raise ValueError('expected fictional UI panel 780x460')
    im=Image.new('RGB',(780,460),'#F8FBFC')
    d=ImageDraw.Draw(im)
    def f(sz): return ImageFont.truetype(FONT,sz)
    def t(x,y,s,sz,color='#1A3546',anchor='mm'):
        d.text((x,y),s,font=f(sz),fill=color,anchor=anchor)
    d.rounded_rectangle((0,0,780,55),radius=7,fill='#1D394B')
    t(390,28,'AI仕事術  /  仕事の進め方',23,'#FFFFFF')
    t(390,96,'まず、仕事を3つに分ける',36)
    d.rounded_rectangle((25,147,366,377),radius=19,fill='#FBEAE6')
    d.rounded_rectangle((414,147,755,377),radius=19,fill='#E3F6F2')
    t(195,184,'BEFORE',27,'#A94C44')
    t(584,184,'AFTER',27,'#147F73')
    t(195,244,'全部を手作業',32)
    t(195,307,'整理も下書きも',25,'#765E5A')
    t(195,341,'自分ひとりで',25,'#765E5A')
    t(584,244,'AIは下書き担当',30)
    t(584,307,'整理 → 下書き',25,'#397B73')
    t(584,341,'最後は人が確認',25,'#397B73')
    d.rounded_rectangle((366,237,416,290),radius=17,fill=accent)
    t(391,264,'→',31,'#FFFFFF')
    t(390,417,'※ AIの出力は必ず人が確認',23,'#526D77')
    return im