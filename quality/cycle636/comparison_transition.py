"""Reusable, original Before/After wipe for portrait video. REVIEW ONLY."""
from PIL import Image, ImageDraw, ImageFont

DEFAULT={'before':('手入力','何度も確認','作業が分散'),
         'after':('数式で集計','結果を検算','手順が明確')}

def ease_out(t):
    t=min(1.,max(0.,float(t)))
    return 1-(1-t)**3

def reveal_fraction(progress):
    return ease_out((float(progress)-0.18)/0.67)

def geometry(progress,box=(65,306,475,630)):
    x0,y0,x1,y1=box
    reveal=reveal_fraction(progress)
    divider=round(x1-(x1-x0)*reveal)
    return {'box':box,'divider':divider,'reveal':reveal,
            'visible_after_pixels':x1-divider}

def draw_transition(image,progress,labels=DEFAULT,
                    font_path='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'):
    if not set(labels)=={'before','after'}: raise ValueError('two sides required')
    if any(len(labels[k])!=3 for k in labels): raise ValueError('three lines per side required')
    g=geometry(progress)
    x0,y0,x1,y1=g['box']; div=g['divider']
    f24=ImageFont.truetype(font_path,24);f20=ImageFont.truetype(font_path,20)
    d=ImageDraw.Draw(image)
    d.text((72,237),'BEFORE  →  AFTER',font=f24,fill=(244,248,252))
    d.rounded_rectangle((x0,y0,x1,y1),radius=20,fill=(66,41,58),outline=(150,75,97),width=3)
    d.rounded_rectangle((x0+16,y0+18,x1-16,y0+68),radius=11,fill=(107,53,69))
    d.text((x0+32,y0+26),'BEFORE / 手作業',font=f20,fill=(255,238,239))
    for i,txt in enumerate(labels['before']):
        yy=y0+103+i*72
        d.rounded_rectangle((x0+22,yy,x1-22,yy+55),radius=11,fill=(89,48,66))
        d.text((x0+42,yy+13),f'×  {txt}',font=f20,fill=(247,225,230))
    after=Image.new('RGBA',image.size,(0,0,0,0));a=ImageDraw.Draw(after)
    a.rounded_rectangle((x0,y0,x1,y1),radius=20,fill=(12,91,91,255),outline=(52,211,190,255),width=3)
    a.rounded_rectangle((x0+16,y0+18,x1-16,y0+68),radius=11,fill=(22,135,127,255))
    a.text((x0+32,y0+26),'AFTER / 数式',font=f20,fill=(246,255,251,255))
    for i,txt in enumerate(labels['after']):
        yy=y0+103+i*72
        a.rounded_rectangle((x0+22,yy,x1-22,yy+55),radius=11,fill=(21,112,109,255))
        a.text((x0+42,yy+13),f'✓  {txt}',font=f20,fill=(243,255,252,255))
    if div<x1:
        part=after.crop((div,y0,x1,y1));image.paste(part,(div,y0),part)
        d=ImageDraw.Draw(image)
        if div>x0:
            d.line((div,y0+5,div,y1-5),fill=(249,218,126),width=5)
            d.ellipse((div-11,y0+140,div+11,y0+162),fill=(249,218,126))
    d=ImageDraw.Draw(image)
    d.rounded_rectangle((78,650,464,700),radius=11,fill=(19,77,96))
    d.text((99,660),'操作の違いを画面で比較',font=f20,fill=(255,220,131))
    return g
