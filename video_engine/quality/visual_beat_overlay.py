"""Reusable visual caption painter (no speech sync)."""
from PIL import ImageDraw

def draw_visual_beat(image, beat, t, font_factory, width=540):
    d=ImageDraw.Draw(image)
    d.rounded_rectangle((26,716,width-26,772),radius=13,fill='#082b4b')
    font=font_factory(29 if len(beat.text)<=14 else 24)
    pre,key,post=beat.text.partition(beat.emphasis)
    parts=((pre,'white'),(key,'#66ffe4'),(post,'white'))
    lengths=[d.textbbox((0,0),v,font=font)[2] if v else 0 for v,c in parts]
    x=(width-sum(lengths))//2
    if x<37:raise ValueError('Caption too wide')
    for (part,color),length in zip(parts,lengths):
        if part:d.text((x,724),part,font=font,fill=color)
        x+=length
    return True
