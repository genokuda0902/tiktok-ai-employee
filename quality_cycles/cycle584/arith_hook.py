"""Cycle584: reproducible, original 9:16 number-proof hook. REVIEW ONLY.

A reusable, genre-independent arithmetic contract prevents visually misleading
intermediate 'total' counters. No user-provided media or confidential assets.
"""
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai_productivity','beauty','relationships','finance','sales','career','health','science','travel','products')
FPS=30
SIZE=(540,960)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

@dataclass(frozen=True)
class Proof:
    genre: str
    items: tuple[int, ...]
    expected: int
    source: str
    verified: bool
    def validate(self):
        if self.genre not in GENRES: raise ValueError('unrecognized genre')
        if not self.verified or not self.source: raise ValueError('no verified evidence')
        if len(self.items)!=4 or any(type(n)!=int or n<0 or n>999 for n in self.items): raise ValueError('invalid values')
        if sum(self.items)!=self.expected: raise ValueError('mismatched result')
        return True
    def running_totals(self):
        self.validate()
        totals=[]; acc=0
        for value in self.items:
            acc+=value;totals.append(acc)
        return tuple(totals)

DEFAULT=Proof('ai_productivity',(120,150,200,250),720,'synthetic verified arithmetic',True)

def font(sz,bold=False): return ImageFont.truetype(BOLD if bold else FONT,sz)
def text(d,xy,s,sz=22,color='#f4ffff',bold=False): d.text(xy,s,font=font(sz,bold),fill=color)
def rr(d,box,fill,outline=None,r=14,width=2): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def progress_at(frame_index):
    """Return 0..4 completed addends; intermediate sums are actual prefix sums."""
    if not 0<=frame_index<60: raise ValueError('frame outside hook')
    if frame_index<18:return 0
    return min(4,1+(frame_index-18)//9)

def state(spec:Proof,index:int):
    totals=spec.running_totals()
    completed=progress_at(index)
    return {'completed':completed,'running_total':None if completed==0 else totals[completed-1],
            'valid_prefix_totals':totals,'final':spec.expected,'synthetic':True}

def frame(spec:Proof,index:int):
    s=state(spec,index)
    im=Image.new('RGB',SIZE,'#061221');d=ImageDraw.Draw(im)
    # Layered original vector art: no third-party photos, logo, or generated identity.
    for y in range(960):
        d.line((0,y,540,y),fill=(6+int(y/170),18+int(y/70),33+int(y/65)))
    for x,y,r in ((440,146,140),(70,380,115),(380,650,155)):
        d.ellipse((x-r,y-r,x+r,y+r),outline='#133c51',width=3)
    rr(d,(25,34,515,97),'#0a3649','#1ad8d0',16)
    text(d,(45,48),'AI時短ラボ  |  20秒で検算',26,bold=True)
    text(d,(27,138),'その合計、合ってる？',36,bold=True)
    text(d,(30,198),'4つの数字を、順番に足す。',22,'#a8e6f0')
    rr(d,(25,264,515,554),'#102a3a','#348aa0',20)
    text(d,(48,286),'入力データ（架空）',23,'#b9dfe8',True)
    for j,v in enumerate(spec.items):
        x=42+j*121
        active=j<s['completed']
        rr(d,(x,349,x+110,475),'#075e64' if active else '#1c3d4d','#31d7cf' if active else '#446779',12)
        text(d,(x+15,367),f'B{j+2}',21,'#d3e5e8')
        text(d,(x+14,413),str(v),26,'#ffffff',True)
        if active:
            d.ellipse((x+83,361,x+100,378),fill='#42f5ba')
    rr(d,(25,581,515,785),'#0a343c','#30cfc6',20)
    text(d,(45,604),'検算中の合計',24,'#b9f4e7',True)
    if s['running_total'] is None:
        text(d,(60,656),'数字を確認…',34,'#d8f7fa',True)
    else:
        # Crucially: only valid prefix totals may be displayed.
        text(d,(70,645),str(s['running_total']),72,'#f4fffc',True)
        text(d,(325,678),f"{s['completed']} / 4",27,'#9ff7df',True)
    rr(d,(25,819,515,908),'#075662','#26c5cb',15)
    text(d,(50,836),'手計算の前に、合計720を確認',26,'#ffffff',True)
    text(d,(25,927),'架空データ  /  REVIEW ONLY  /  NOT APPROVED',14,'#b2c5d5')
    return im
