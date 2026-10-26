"""Minimal reusable 9:16 layout core for cycle873; no external dependencies."""
from dataclasses import dataclass
W,H,FPS=1080,1920,30
DURATION=691/FPS
CAPTION_TOP=1480
GENRES={
'ai_productivity':('AI・仕事効率化','#29C7B2'),
'beauty':('美容・身だしなみ','#EE8EB4'),
'romance_psychology':('恋愛・心理','#E78BA6'),
'money_saving':('お金・節約','#78BE93'),
'sales_business':('営業・ビジネス','#6D91D7'),
'career':('転職・キャリア','#8E91D6'),
'health_lifestyle':('健康・生活改善','#6BA9D9'),
'trivia_science':('雑学・科学','#A68DF4'),
'travel_food':('旅行・グルメ','#5B9DD6'),
'product_lifestyle':('商品比較・暮らし','#E9B85F'),
}
SCENES=((0,3.1),(3.1,5.85),(5.85,8.45),(8.45,11.35),(11.35,14.2),(14.2,17.25),(17.25,19.85),(19.85,DURATION))
CROP=(0,145,1080,1145)
DEST=(35,440,1045,1375)
SOURCE_UI=(35,155,1025,1125)
@dataclass(frozen=True)
class Rect:
    x0:int;y0:int;x1:int;y1:int
    @property
    def w(self):return self.x1-self.x0
    @property
    def h(self):return self.y1-self.y0
    def contains(self,other):return self.x0<=other.x0 and self.y0<=other.y0 and self.x1>=other.x1 and self.y1>=other.y1
def validate_layout(crop=CROP,dest=DEST,ui=SOURCE_UI,genre='ai_productivity'):
    if genre not in GENRES:raise ValueError('Unknown genre')
    c,d,u=Rect(*crop),Rect(*dest),Rect(*ui)
    if min(c.w,c.h,d.w,d.h,u.w,u.h)<=0:raise ValueError('Nonpositive dimensions')
    if not Rect(0,0,W,H).contains(c) or not c.contains(u):raise ValueError('Critical UI clipped')
    if not Rect(0,0,W,CAPTION_TOP).contains(d):raise ValueError('Caption collision')
    if abs(c.w/c.h-d.w/d.h)>.035:raise ValueError('UI distortion')
    return True
def validate_scenes(scenes=SCENES):
    if len(scenes)!=8 or abs(scenes[0][0])>1e-6 or abs(scenes[-1][1]-DURATION)>1e-4:raise ValueError('Scene coverage')
    for i,(a,b) in enumerate(scenes):
        if a>=b or (i and abs(scenes[i-1][1]-a)>1e-6):raise ValueError('Scene gap/overlap')
    return True
def validate_beats(beats):
    if len(beats)!=24:raise ValueError('Expected 24 captions')
    for b in beats:
        if not b['text'].strip() or not 0<=b['start']<b['end']<=DURATION+.01:raise ValueError('Bad caption')
    if any(beats[i]['end']>beats[i+1]['start'] for i in range(len(beats)-1)):raise ValueError('Overlapping captions')
    return True
