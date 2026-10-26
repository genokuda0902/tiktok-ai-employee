"""Cycle871 portable 10-genre layout and subtitle validation (offline, review only)."""
from dataclasses import dataclass

W,H,FPS=1080,1920,30
DURATION=691/FPS
GENRES={
 'ai_productivity':'#29C7B2','trivia':'#A68DF4','cooking':'#F3A35C',
 'beauty':'#EE8EB4','money':'#78BE93','health':'#6BA9D9',
 'travel':'#5B9DD6','product_review':'#E9B85F',
 'story':'#AF84D8','work_skills':'#6D91D7'}
SCENES=((0,3.1),(3.1,5.85),(5.85,8.45),(8.45,11.35),
        (11.35,14.2),(14.2,17.25),(17.25,19.85),(19.85,DURATION))
SOURCE_W,SOURCE_H=1080,1920
SOURCE_UI=(35,155,1025,1125)
CROP=(0,145,1080,1145)
DEST=(35,440,1045,1375)
CAPTION_TOP=1480

@dataclass(frozen=True)
class Rect:
    x0:int;y0:int;x1:int;y1:int
    @property
    def w(self):return self.x1-self.x0
    @property
    def h(self):return self.y1-self.y0
    def contains(self,other):
        return self.x0<=other.x0 and self.y0<=other.y0 and self.x1>=other.x1 and self.y1>=other.y1

def validate_layout(crop=CROP,dest=DEST,ui=SOURCE_UI,genre='ai_productivity'):
    if genre not in GENRES:raise ValueError('Unknown genre')
    c,d,u=Rect(*crop),Rect(*dest),Rect(*ui)
    if min(c.w,c.h,d.w,d.h,u.w,u.h)<=0:raise ValueError('Nonpositive dimension')
    if not Rect(0,0,SOURCE_W,SOURCE_H).contains(c):raise ValueError('Crop outside source')
    if not c.contains(u):raise ValueError('Critical UI content clipped')
    if not Rect(0,0,W,CAPTION_TOP).contains(d):raise ValueError('Subtitle collision or output bounds')
    if abs(c.w/c.h-d.w/d.h)>0.035:raise ValueError('Stretching UI beyond tolerance')
    return True

def validate_scenes(scenes=SCENES):
    if len(scenes)!=8:raise ValueError('Need eight scenes')
    if abs(scenes[0][0])>1e-6 or abs(scenes[-1][1]-DURATION)>1e-4:raise ValueError('Duration mismatch')
    for i,(a,b) in enumerate(scenes):
        if a>=b or (i and abs(scenes[i-1][1]-a)>1e-6):raise ValueError('Scene gap/overlap')
    return True

def validate_beats(beats):
    if len(beats)!=24:raise ValueError('Expected 24 Japanese subtitle beats')
    for beat in beats:
        if not isinstance(beat['text'],str) or not beat['text'].strip():raise ValueError('Empty subtitle')
        if not 0<=beat['start']<beat['end']<=DURATION+0.01:raise ValueError('Bad subtitle time')
    if any(beats[i]['end']>beats[i+1]['start'] for i in range(len(beats)-1)):
        raise ValueError('Subtitle overlaps')
    return True
