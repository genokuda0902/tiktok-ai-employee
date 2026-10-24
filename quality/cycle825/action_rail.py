"""Shared viewer-facing action rail for both full and CI slide compositors.
Original graphics only. No network, PII, publishing or tracking.
"""
from PIL import ImageDraw, ImageFont

PALETTES={
 'ai_work':'#38C6C0','beauty':'#D96C96','love_psychology':'#9B86D9',
 'money_saving':'#D8A24A','sales_business':'#19A58B','career':'#6D8FDF',
 'health_life':'#81B479','science':'#41A6CC','travel_food':'#DF9562',
 'product_life':'#A985D2',
}
ACTIONS=[
 '作業を3つに分けてみる','繰り返す作業を1つ選ぶ',
 '完成見本を1つ用意する','目的・条件・見本を書く',
 '日付・数字・根拠を確認','修正点を1つだけ伝える',
 '使えた指示を保存する','明日も1つ試してみる',
]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def apply_action_rail(image, index, genre='ai_work'):
    """Return RGBA image with the same lower-third layout in every renderer."""
    if genre not in PALETTES or not 0<=index<8:
        raise ValueError('unknown genre or invalid scene')
    accent=PALETTES[genre]
    im=image.convert('RGBA')
    d=ImageDraw.Draw(im)
    d.rectangle((0,1315,1080,1920),fill='#0D2434')
    d.rectangle((0,1315,1080,1324),fill=accent)
    d.rounded_rectangle((66,1360,274,1418),radius=22,fill=accent)
    def write(xy,value,size,color,anchor='lm'):
        d.text(xy,value,font=ImageFont.truetype(FONT,size),fill=color,anchor=anchor)
    write((170,1388),f'STEP {index+1:02} / 08',24,'#092F3B','mm')
    for k in range(8):
        x=714+k*35
        d.ellipse((x,1377,x+18,1395),fill=accent if k<=index else '#42606C')
    d.line((92,1720,988,1720),fill='#34535F',width=2)
    write((90,1771),'今日のアクション',27,accent)
    write((90,1835),ACTIONS[index],38,'#F0F7F8')
    return im
