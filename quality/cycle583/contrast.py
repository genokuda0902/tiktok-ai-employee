"""cycle583: original genre-neutral, verified problem/solution scene. No external assets."""
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

FPS=30
SIZE=(540,960)
GENRES=('ai_productivity','beauty','relationships','finance','sales','career','health','science','travel','products')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

@dataclass(frozen=True)
class ContrastSpec:
    genre:str
    problem:str
    method:str
    evidence:str
    result:str
    verified:bool=False
    def validate(self):
        if self.genre not in GENRES: raise ValueError('unknown genre')
        if not self.verified: raise ValueError('unverified claim')
        for s in (self.problem,self.method,self.evidence,self.result):
            if not s or len(s)>26 or '\n' in s: raise ValueError('invalid text')
        return True

DEFAULT=ContrastSpec('ai_productivity','毎回、数字を手で合計','SUM関数で検算','120＋150＋200＋250','720',True)

def f(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def txt(d,xy,s,size=24,color='#f2f8ff',bold=False):d.text(xy,s,font=f(size,bold),fill=color)
def box(d,xy,fill,outline=None,r=18):d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=2)

def frame(spec:ContrastSpec,index:int):
    spec.validate()
    if not 0<=index<60:raise ValueError('frame outside segment')
    t=index/FPS
    im=Image.new('RGB',SIZE,'#061426');d=ImageDraw.Draw(im)
    for y in range(960):
        p=y/960
        d.line((0,y,540,y),fill=(int(7+8*p),int(22+12*p),int(39+23*p)))
    box(d,(26,30,514,94),'#0d3149','#2dc7df',14)
    txt(d,(46,45),'02  入力から検算へ',29,bold=True)
    txt(d,(30,123),'同じ数字を、どう扱う？',28,bold=True)
    box(d,(26,193,514,359),'#332c3b','#ed9a81')
    box(d,(42,210,168,252),'#9b493f')
    txt(d,(58,216),'BEFORE',19,bold=True)
    txt(d,(46,266),spec.problem,26,bold=True)
    txt(d,(47,308),'120   150   200   250',22,'#ffe5d9',True)
    box(d,(26,391,514,724),'#102f3b','#29d2c5')
    box(d,(42,408,160,450),'#087969')
    txt(d,(54,414),'AFTER',19,bold=True)
    txt(d,(44,466),spec.method,27,'#c9fff5',True)
    for j,v in enumerate((120,150,200,250)):
        x=43+j*120
        fill='#1e6b74' if t >= .15+j*.16 else '#25434e'
        box(d,(x,529,x+104,606),fill,'#67b4bd',10)
        txt(d,(x+13,538),f'B{j+2}',17,'#a9d9e0')
        txt(d,(x+14,564),str(v),23,bold=True)
    if t>=.55:
        box(d,(44,622,496,696),'#f4fafb')
        formula='=SUM(B2:B5)'
        shown=max(1,min(len(formula),int((t-.55)*18)))
        txt(d,(62,639),formula[:shown],27,'#12475c',True)
    if t>=1.23:
        box(d,(49,744,491,817),'#076b62','#64f4d5',15)
        txt(d,(80,755),f'検算結果  {spec.result}',31,bold=True)
    else:
        box(d,(49,744,491,817),'#17374b')
        txt(d,(77,762),'数値を確認しています',23,'#c3e4ee')
    box(d,(18,844,522,910),'#075361','#2fd2ce',12)
    txt(d,(48,859),'4か月分の売上を入力',26,bold=True)
    txt(d,(24,932),'架空データ / REVIEW ONLY / NOT APPROVED',14,'#a6c4d4')
    return im
