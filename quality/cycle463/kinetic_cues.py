"""Reusable, genre-neutral kinetic cue for synthetic TikTok review renders.
Never implies publication approval or Japanese narration availability.
"""
from dataclasses import dataclass
from PIL import ImageDraw, ImageFont

@dataclass(frozen=True)
class Cue:
    tag: str
    color: str

CUES = {
    'hook': Cue('01 / HOOK', '#ffd99c'),
    'before': Cue('02 / BEFORE', '#ffbfa5'),
    'data': Cue('03 / INPUT', '#8ee6e4'),
    'formula': Cue('04 / ACTION', '#8ee6e4'),
    'proof': Cue('05 / EVIDENCE', '#b7f0a5'),
    'result': Cue('06 / RESULT', '#b7f0a5'),
    'compare': Cue('07 / CHANGE', '#ffd99c'),
    'cta': Cue('08 / SAVE', '#8ee6e4'),
}

def ease(p):
    p=max(0.,min(1.,p))
    return p*p*(3-2*p)

def apply_cue(frame, kind, local_progress, font_path):
    if kind not in CUES: raise ValueError(f'unknown scene: {kind}')
    if not 0 <= local_progress <= 1: raise ValueError('progress out of range')
    cue=CUES[kind]
    d=ImageDraw.Draw(frame)
    p=ease(local_progress)
    y=255+round(24*(1-ease(min(1,local_progress*6))))
    d.rounded_rectangle((40,y,294,y+56),radius=14,fill='#0b2538',outline=cue.color,width=3)
    font=ImageFont.truetype(font_path,24)
    d.text((58,y+11),cue.tag,font=font,fill=cue.color)
    d.rounded_rectangle((308,275,670,292),radius=8,fill='#24495c')
    x=308+round(362*p)
    d.rounded_rectangle((308,275,max(309,x),292),radius=8,fill=cue.color)
    d.ellipse((x-10,273,x+10,294),fill='#f7ffff')
    return frame

def safe_bounds(caption_top=1010):
    return 255 >= 0 and 321 < caption_top
