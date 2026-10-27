"""Cycle896: local-only, genre-neutral native Japanese 3-step prompt panel."""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE=(1080,1920)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SAFE_CARD=(65,325,1015,1200)

@dataclass(frozen=True)
class PromptSpec:
    title: str
    fields: tuple[tuple[str,str],...]
    note: str='架空のローカル画面・送信なし'
    def validate(self):
        if len(self.fields)!=3 or not self.title:
            raise ValueError('title and exactly three fields required')
        if any(not label or not value for label,value in self.fields):
            raise ValueError('empty field')
        if len(self.title)>17 or len(self.note)>22:
            raise ValueError('title/note too long')
        if any(len(label)>6 or len(value)>17 for label,value in self.fields):
            raise ValueError('field too long')

def font(size,bold=False):
    return ImageFont.truetype(BOLD if bold else FONT,size,index=0)

def fit(draw,pos,text,max_width,start,color,bold=False,minimum=30):
    for size in range(start,minimum-1,-1):
        f=font(size,bold)
        if draw.textbbox((0,0),text,font=f)[2]<=max_width:
            draw.text(pos,text,font=f,fill=color)
            return size
    raise ValueError('text cannot fit: '+text)

def render(spec:PromptSpec,active:int)->Image.Image:
    spec.validate()
    if active not in (0,1,2):
        raise ValueError('active must be 0,1,2')
    im=Image.new('RGBA',SIZE,(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle(SAFE_CARD,radius=42,fill=(245,249,255,255))
    d.rounded_rectangle((94,354,986,471),radius=26,fill=(220,238,255,255))
    fit(d,(120,371),spec.title,770,59,(13,51,91,255),True)
    d.rounded_rectangle((819,380,956,440),radius=24,fill=(15,115,211,255))
    fit(d,(842,387),f'{active+1} / 3',100,33,(255,255,255,255),True)
    for i,(label,value) in enumerate(spec.fields):
        top=508+i*184
        selected=i==active
        completed=i<active
        border=(19,187,163,255) if selected else (197,215,234,255)
        bg=(222,250,243,255) if selected else (255,255,255,255)
        d.rounded_rectangle((105,top,975,top+162),radius=22,fill=bg,outline=border,width=6 if selected else 3)
        d.ellipse((127,top+52,189,top+114),fill=(16,177,150,255) if completed else (17,124,224,255) if selected else (189,203,221,255))
        fit(d,(145,top+59),'✓' if completed else str(i+1),35,36,(255,255,255,255),True)
        fit(d,(220,top+16),label,600,39,(33,102,171,255),True)
        fit(d,(220,top+75),value,700,44,(20,46,79,255),selected,minimum=32)
        if selected:
            d.rounded_rectangle((922,top+113,956,top+145),radius=6,fill=(19,187,163,255))
    d.rounded_rectangle((111,1086,969,1156),radius=19,fill=(222,234,247,255))
    fit(d,(141,1100),spec.note,790,34,(55,86,121,255))
    return im

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True)
    p.add_argument('--spec')
    a=p.parse_args()
    if a.spec:
        raw=json.loads(Path(a.spec).read_text(encoding='utf-8'))
        spec=PromptSpec(raw['title'],tuple(tuple(x) for x in raw['fields']),raw.get('note','架空のローカル画面・送信なし'))
    else:
        spec=PromptSpec('目的と条件を3つに整理',(('目的','上司への週次報告'),('条件','数字と根拠を入れる'),('形式','箇条書き3点')))
    out=Path(a.output)
    out.mkdir(parents=True,exist_ok=True)
    for i in range(3):
        render(spec,i).save(out/f'prompt_state_{i+1}.png',optimize=True)
    print(json.dumps({'states':3,'resolution':SIZE,'review_only':True},ensure_ascii=False))

if __name__=='__main__':
    main()
