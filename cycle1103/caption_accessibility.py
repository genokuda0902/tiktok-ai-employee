"""Native-resolution Japanese caption plates for REVIEW ONLY. No posting.

Captions below were transcribed from *visible existing captions*, not ASR.
Speech meaning and word timing are NOT verified. Ten palette presets.
"""
from PIL import Image, ImageDraw, ImageFont

CAPTIONS = [
    ("AIで仕事を早くするなら、", "最初の一歩が大事。"),
    ("まず、繰り返している作業を", "書き出す。"),
    ("次に、完成形の見本を", "用意する。"),
    ("指示は、目的と条件を", "具体的に伝える。"),
    ("最初の出力は、", "必ず自分で確かめる。"),
    ("違いがあれば、修正点を", "一つずつ伝える。"),
    ("使える指示は、", "テンプレートに残す。"),
    ("小さな時短を、", "毎日の習慣にしよう。"),
]
GENRE_PALETTES = {
    'ai_work': ('#36ddcb','#0c1c2b'), 'money': ('#ffd166','#241d15'),
    'health': ('#72e3b0','#12251f'), 'beauty': ('#ffb7d5','#281b26'),
    'education': ('#7eb9ff','#17243a'), 'travel': ('#f3c777','#2b2118'),
    'food': ('#ffad79','#2d201a'), 'lifestyle': ('#b8a5ff','#201d31'),
    'psychology': ('#9cdeef','#142833'), 'business': ('#81ddf7','#142331'),
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SMALL_FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def render_plate(index, genre='ai_work', size=(1080,1920), font_path=FONT):
    if genre not in GENRE_PALETTES: raise ValueError('unknown genre')
    if index < 0 or index >= len(CAPTIONS): raise ValueError('bad chapter index')
    if size != (1080,1920): raise ValueError('only 1080x1920 supported')
    accent, _ = GENRE_PALETTES[genre]
    im=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(im)
    # Opaque old subtitle replacement, safely above learning rail at y=1630.
    d.rounded_rectangle((44,1370,1036,1615),radius=25,fill=(6,13,27,255),
                        outline=(75,125,143,255),width=3)
    d.rounded_rectangle((57,1394,67,1588),radius=5,fill=accent)
    d.text((92,1385),f'JAPANESE CAPTION  •  {index+1:02d}/08',
           font=ImageFont.truetype(SMALL_FONT,22),fill=(135,185,199,255))
    font=ImageFont.truetype(font_path,64)
    for j,line in enumerate(CAPTIONS[index]):
        box=d.textbbox((0,0),line,font=font)
        width=box[2]-box[0]
        if width>888: raise ValueError('caption overflow')
        d.text(((1080-width)//2,1431+j*78),line,font=font,
               fill=(255,255,255,255) if j==0 else accent)
    return im
