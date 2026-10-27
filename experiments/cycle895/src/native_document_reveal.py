"""Cycle895: native Japanese document sample; 3 progressive highlights."""
import argparse,json
from dataclasses import dataclass
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
SIZE=(1080,1920)
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
@dataclass(frozen=True)
class DocumentSpec:
    title:str
    rows:tuple
    badge:str='サンプル・架空の画面'
    def validate(self):
        if not 1<=len(self.rows)<=3:raise ValueError('1-3 rows required')
        if not self.title or any(not a or not b for a,b in self.rows):raise ValueError('empty text')
        if len(self.title)>20 or any(len(a)>12 or len(b)>18 for a,b in self.rows):raise ValueError('text exceeds mobile limits')
def font(s,bold=False):return ImageFont.truetype(BOLD if bold else REG,s,index=0)
def fit(d,xy,txt,max_width,size,fill,bold=False,min_size=32):
    for s in range(size,min_size-1,-1):
        f=font(s,bold)
        if d.textbbox((0,0),txt,font=f)[2]<=max_width:
            d.text(xy,txt,font=f,fill=fill)
            return
    raise ValueError('text does not fit')
def render(spec,active):
    spec.validate()
    if not 0<=active<len(spec.rows):raise ValueError('invalid active')
    im=Image.new('RGBA',SIZE,(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((95,420,985,1165),radius=36,fill=(247,250,255,255),outline=(188,210,232,255),width=5)
    d.rounded_rectangle((120,450,960,560),radius=22,fill=(225,239,253,255))
    fit(d,(154,472),spec.title,755,61,(16,42,76),True)
    for i,(label,value) in enumerate(spec.rows):
        y=585+i*150;sel=i==active
        bg=(223,250,244,255) if sel else (255,255,255,255)
        stroke=(16,186,159,255) if sel else (210,222,235,255)
        d.rounded_rectangle((120,y,960,y+130),radius=18,fill=bg,outline=stroke,width=7 if sel else 3)
        d.ellipse((141,y+40,189,y+88),fill=(0,175,151,255) if sel else (172,190,209,255))
        d.text((155,y+43),str(i+1),font=font(30,True),fill=(255,255,255,255))
        fit(d,(213,y+16),label,680,42,(22,105,184),True)
        fit(d,(213,y+70),value,680,39,(25,43,66))
    d.rounded_rectangle((128,1068,520,1120),radius=14,fill=(224,234,246,255))
    fit(d,(145,1075),spec.badge,354,26,(63,85,115),min_size=24)
    return im
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    spec=DocumentSpec('週次報告｜見本',(('今週の成果','要点を3つに整理'),('気づき','数字と根拠を明記'),('次の行動','担当と期限を記載')))
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    for i in range(3):render(spec,i).save(out/f'document_state_{i+1}.png',optimize=True)
    print(json.dumps({'states':3,'size':SIZE},ensure_ascii=False))
