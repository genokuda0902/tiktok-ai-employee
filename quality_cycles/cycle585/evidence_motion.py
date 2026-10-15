"""cycle585: original synthetic, evidence-first graph motion. No private inputs.

Reusable across genres; strict evidence/rights contract, no invented intermediate
values, no data inferred from a chart screenshot. For human review only.
"""
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

GENRES = ('ai_productivity','beauty','relationships','finance','sales','career','health','science','travel','products')
FPS = 30
SIZE = (540, 960)
VALUES = (120,150,200,250)
LABELS = ('1月','2月','3月','4月')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

@dataclass(frozen=True)
class Evidence:
    genre: str
    labels: tuple[str,...]
    values: tuple[int,...]
    source: str
    synthetic: bool
    rights: str
    def validate(self):
        if self.genre not in GENRES: raise ValueError('unrecognized genre')
        if not self.synthetic: raise ValueError('not a synthetic public-safe demonstration')
        if self.rights != 'original_code_generated': raise ValueError('unapproved visual rights')
        if not self.source.strip(): raise ValueError('missing provenance')
        if len(self.labels) != 4 or len(self.values) != 4: raise ValueError('four evidence points required')
        if len(set(self.labels)) != 4: raise ValueError('duplicate labels')
        if any(type(v) is not int or not 0 <= v <= 999 for v in self.values): raise ValueError('invalid values')
        if any(not s or len(s)>8 for s in self.labels): raise ValueError('invalid labels')
        return True

DEMO = Evidence('ai_productivity',LABELS,VALUES,'synthetic source: (120,150,200,250)',True,'original_code_generated')

def smooth(x):
    x=max(0,min(1,x))
    return x*x*(3-2*x)

def bar_progress(frame_index, j):
    """One-at-a-time growth. 1.0 means final number is safe to display."""
    if not 0 <= frame_index < 120: raise ValueError('frame outside segment')
    return smooth((frame_index-(10+j*17))/15)

def bar_state(spec, index):
    spec.validate()
    progresses=[bar_progress(index,j) for j in range(4)]
    done=[p >= 1 for p in progresses]
    return {
        'bar_progress':progresses,
        'visible_values':[v if is_done else None for v,is_done in zip(spec.values,done)],
        'all_verified':all(done),
        'total':sum(spec.values) if all(done) else None,
    }

def font(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)

def txt(draw,xy,s,size=24,fill='#effbff',bold=False):
    draw.text(xy,s,font=font(size,bold),fill=fill,stroke_width=0)

def rect(draw,box,fill,outline=None,r=12,width=2):
    draw.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def frame(spec,index):
    st=bar_state(spec,index)
    img=Image.new('RGB',SIZE,'#061523');d=ImageDraw.Draw(img)
    # Original vector-only illustration with coherent color hierarchy.
    for y in range(960):
        d.line((0,y,540,y),fill=(6+int(y/320),20+int(y/125),34+int(y/105)))
    d.ellipse((360,-80,740,300),outline='#113b52',width=5)
    d.ellipse((-180,460,260,920),outline='#143c53',width=4)
    rect(d,(20,28,520,98),'#0c3044','#35cfd1',14)
    txt(d,(42,45),'06   DATA → VISUAL PROOF',25,'#f0ffff',True)
    txt(d,(22,131),'数字からグラフへ。',35,'#ffffff',True)
    txt(d,(24,188),'4つの数値を、そのまま可視化',22,'#98d9e5')
    rect(d,(20,248,520,407),'#0b2939','#317b8a',16)
    txt(d,(38,267),'SOURCE  |  元データ（架空）',21,'#a8e9ed',True)
    for j,(lab,val) in enumerate(zip(spec.labels,spec.values)):
        x=36+j*123
        rect(d,(x,313,x+112,384),'#174254','#306a78',10)
        txt(d,(x+8,320),lab,19,'#a8d2db')
        txt(d,(x+8,344),str(val),25,'#ffffff',True)
    rect(d,(20,433,520,802),'#0d293b','#2c6679',17)
    txt(d,(40,455),'GRAPH  |  売上推移',23,'#ffffff',True)
    # y=720 baseline, y=525 corresponds to 250.
    left=65; right=493; top=535; bottom=723
    for mark in (0,125,250):
        yy=bottom-round(mark/250*(bottom-top))
        d.line((left,yy,right,yy),fill='#2c4e61',width=2)
        txt(d,(26,yy-13),str(mark),14,'#88acbb')
    for j,(label,value) in enumerate(zip(spec.labels,spec.values)):
        x=89+j*104
        h=int((value/250)*185*st['bar_progress'][j])
        if h:
            # shadow plus a strong, clean primary bar
            rect(d,(x+3,bottom-h+3,x+66,bottom+2),'#174553',r=8)
            rect(d,(x,bottom-h,x+62,bottom),'#20b7c4','#6ce7e3',r=7,width=1)
            if st['visible_values'][j] is not None:
                txt(d,(x+3,bottom-h-37),str(value),25,'#ffffff',True)
        txt(d,(x+7,742),label,20,'#cce6ef',True)
    rect(d,(20,824,520,910),'#08414c','#27c6c7',15)
    if st['all_verified']:
        txt(d,(42,837),f'120 + 150 + 200 + 250 = {st["total"]}',26,'#ffffff',True)
        txt(d,(43,876),'4本の棒と元データが一致 ✓',18,'#9fffe1')
    else:
        txt(d,(43,838),'元データと棒グラフを照合中…',25,'#ffffff',True)
        txt(d,(43,878),'表示した数値だけを検証',18,'#a1e3ed')
    txt(d,(22,930),'架空データ  |  REVIEW ONLY  |  NOT APPROVED',14,'#b6c7d1')
    return img
