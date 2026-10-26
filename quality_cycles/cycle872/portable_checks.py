"""Cycle872 portable layout and subtitle checks; no source assets or uploads."""
from dataclasses import dataclass

W,H,FPS=1080,1920,30
FRAMES=691
DURATION=FRAMES/FPS
CAPTION_TOP=1480
GENRES={
 "ai_productivity":"AI・仕事効率化",
 "beauty":"美容・身だしなみ",
 "romance_psychology":"恋愛・心理",
 "money_saving":"お金・節約",
 "sales_business":"営業・ビジネス",
 "career":"転職・キャリア",
 "health_lifestyle":"健康・生活改善",
 "trivia_science":"雑学・科学",
 "travel_food":"旅行・グルメ",
 "product_lifestyle":"商品比較・暮らし",
}
SCENES=((0,3.1),(3.1,5.85),(5.85,8.45),(8.45,11.35),
        (11.35,14.2),(14.2,17.25),(17.25,19.85),(19.85,DURATION))
PORTRAITS={1:(715,218,1005,543),8:(748,222,998,532)}
TITLE=(62,265,670,550)
CROP=(0,145,1080,1145)
SOURCE_UI=(35,155,1025,1125)
DEST=(35,440,1045,1375)

@dataclass(frozen=True)
class Rect:
    x0:int;y0:int;x1:int;y1:int
    @property
    def w(self): return self.x1-self.x0
    @property
    def h(self): return self.y1-self.y0
    def contains(self,other):
        return self.x0<=other.x0 and self.y0<=other.y0 and self.x1>=other.x1 and self.y1>=other.y1
    def intersects(self,other):
        return self.x0<other.x1 and self.x1>other.x0 and self.y0<other.y1 and self.y1>other.y0

def check_layout(crop=CROP,ui=SOURCE_UI,dest=DEST,genre="ai_productivity"):
    if genre not in GENRES: raise ValueError("unknown genre")
    c,u,d=Rect(*crop),Rect(*ui),Rect(*dest)
    if min(c.w,c.h,u.w,u.h,d.w,d.h)<=0: raise ValueError("nonpositive dimensions")
    if not Rect(0,0,W,H).contains(c) or not c.contains(u): raise ValueError("source UI clipped")
    if not Rect(0,0,W,CAPTION_TOP).contains(d): raise ValueError("caption collision")
    if abs(c.w/c.h-d.w/d.h)>.035: raise ValueError("source UI stretched")
    title=Rect(*TITLE)
    for box in PORTRAITS.values():
        photo=Rect(*box)
        if not Rect(0,0,W,CAPTION_TOP).contains(photo): raise ValueError("portrait outside safe zone")
        if title.intersects(photo): raise ValueError("portrait covers headline")
    return True

def check_scenes(scenes=SCENES):
    if len(scenes)!=8 or abs(scenes[0][0])>1e-6 or abs(scenes[-1][1]-DURATION)>1e-4:
        raise ValueError("wrong scenes or duration")
    for i,(start,end) in enumerate(scenes):
        if start>=end or (i and abs(scenes[i-1][1]-start)>1e-6):
            raise ValueError("scene gap or overlap")
    return True

def check_captions(beats):
    if len(beats)!=24: raise ValueError("24 Japanese subtitle beats required")
    for i,b in enumerate(beats):
        if not isinstance(b["text"],str) or not b["text"].strip(): raise ValueError("empty subtitle")
        if not 0<=b["start"]<b["end"]<=DURATION+.01: raise ValueError("invalid time")
        if i and beats[i-1]["end"]>b["start"]: raise ValueError("overlapping subtitle")
    return True

def check_media_probe(probe):
    streams=probe["streams"]
    v=next(s for s in streams if s["codec_type"]=="video")
    a=next(s for s in streams if s["codec_type"]=="audio")
    if (v["codec_name"],v["width"],v["height"],v["r_frame_rate"],int(v["nb_frames"]))!=("h264",W,H,"30/1",FRAMES):
        raise ValueError("wrong video properties")
    if (a["codec_name"],a["sample_rate"])!=("aac","48000"): raise ValueError("wrong audio")
    if abs(float(probe["format"]["duration"])-DURATION)>.02: raise ValueError("wrong duration")
    return True
