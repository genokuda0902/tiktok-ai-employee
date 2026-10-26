"""Reusable zero-cost native-resolution 8-scene TikTok editorial storyboard core.
All media remains HUMAN_REVIEW and must not be automatically published.
"""
from dataclasses import dataclass
from typing import Sequence
W,H=1080,1920
TOP_SAFE=155
BOTTOM_CONTENT=1620
SUBTITLE_BOX=(68,1370,1012,1585)
GENRE_COLORS={
 'ai_productivity':'#4EE0C5','career':'#F6AE68','money':'#82DBAA',
 'health':'#7ECDF8','learning':'#BCA6FF','beauty':'#F7A3C5',
 'travel':'#79C8F8','food':'#F6B778','home':'#A6DC8D','business':'#84A9FF',
}
SCENES=[
 ('AIで仕事を','もっと早く。','今日から始める、8つのステップ'),
 ('繰り返す仕事を','1つ選ぶ。','まずは作業を棚卸し'),
 ('完成の見本を','先に決める。','理想の仕上がりを見せる'),
 ('目的と条件を','具体的に。','指示は3つの要素に分ける'),
 ('最初の出力は','必ず確認。','数字・名前・日付を点検'),
 ('修正点は','1つずつ。','Before → After を見比べる'),
 ('使える指示は','型にして保存。','毎回ゼロから書かない'),
 ('小さな時短を','毎日の習慣に。','保存して、明日ひとつ試す'),
]
CUTS=[0,3.2,5.75,8.4,11.3,14.2,17.2,19.8,23.033333]
@dataclass(frozen=True)
class Slide:
    title1:str
    title2:str
    sub:str

def validate_storyboard(scenes:Sequence[tuple],cuts:Sequence[float],genre:str):
    if genre not in GENRE_COLORS: raise ValueError('unsupported genre')
    if len(scenes)!=8 or len(cuts)!=9: raise ValueError('must contain 8 scenes')
    if cuts[0]!=0 or abs(cuts[-1]-23.033333)>0.01: raise ValueError('bad duration')
    if any(b<=a for a,b in zip(cuts,cuts[1:])): raise ValueError('nonincreasing cuts')
    if len({tuple(s) for s in scenes})!=8: raise ValueError('repeated slide')
    if any(len(s)!=3 or any(not x for x in s) for s in scenes): raise ValueError('invalid slide')
    x1,y1,x2,y2=SUBTITLE_BOX
    if not(0<x1<x2<W and TOP_SAFE<y1<y2<BOTTOM_CONTENT): raise ValueError('subtitle unsafe')
    return True

def pct(done,total):
    if not isinstance(done,int) or not isinstance(total,int) or total<=0 or not 0<=done<=total:
        raise ValueError('invalid completion data')
    return round(done/total*100)
