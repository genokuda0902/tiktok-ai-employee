"""Offline, ten-genre hybrid video compositor configuration. Review-only."""
from dataclasses import dataclass

GENRES = {
    'ai_productivity':'#4EE0C5',  # AI時短
    'trivia':'#BCA6FF',           # 雑学
    'cooking':'#F6B778',          # 料理
    'beauty':'#F7A3C5',           # 美容
    'money':'#82DBAA',            # お金
    'health':'#7ECDF8',           # 健康
    'travel':'#79C8F8',           # 旅行
    'product_review':'#FFC77D',   # 商品紹介
    'story':'#D6A6F8',           # ストーリー
    'work_skills':'#84A9FF',     # 仕事術
}
W, H, FPS = 1080, 1920, 30
VIDEO_SECONDS = 23.033333
CAPTION_Y0 = 1365

@dataclass(frozen=True)
class Crop:
    x: int = 80
    y: int = 320
    w: int = 800
    h: int = 760

@dataclass(frozen=True)
class Placement:
    x: int = 90
    y: int = 510
    w: int = 900
    h: int = 846

@dataclass(frozen=True)
class Segment:
    start: float = 8.4
    end: float = 17.2

def validate(genre='ai_productivity', crop=Crop(), place=Placement(), segment=Segment(),
             source_w=W, source_h=H, duration=VIDEO_SECONDS):
    if genre not in GENRES: raise ValueError('unknown genre')
    if min(crop.x,crop.y,crop.w,crop.h)<0 or not crop.w or not crop.h: raise ValueError('invalid crop')
    if crop.x+crop.w>source_w or crop.y+crop.h>source_h: raise ValueError('crop exceeds source')
    if min(place.x,place.y,place.w,place.h)<0 or not place.w or not place.h: raise ValueError('invalid placement')
    if place.x+place.w>W or place.y+place.h>=CAPTION_Y0: raise ValueError('caption collision')
    if abs(crop.w/crop.h-place.w/place.h)>0.02: raise ValueError('distorted aspect ratio')
    if not 0<=segment.start<segment.end<=duration: raise ValueError('invalid segment')
    return True

def overlay_filter(place=Placement()):
    """Three focus crops: input, numeric proof, revised report.
    The source is a local Chromium interaction recording with synthetic data.
    """
    validate(crop=Crop(y=320),place=place,segment=Segment(8.4,11.3))
    validate(crop=Crop(y=540),place=place,segment=Segment(11.3,14.2))
    validate(crop=Crop(y=540),place=place,segment=Segment(14.2,17.2))
    crops=[(320,8.4,11.3),(540,11.3,14.2),(540,14.2,17.2)]
    parts=["[0:v]drawbox=x=60:y=510:w=960:h=852:color=0x071923:t=fill:enable='gte(t,8.4)*lt(t,17.2)'[base]",'[1:v]split=3[d0][d1][d2]']
    for i,(y,_,_) in enumerate(crops):
        parts.append(f'[d{i}]crop=800:760:80:{y},scale={place.w}:{place.h}:flags=lanczos,setsar=1[zoom{i}]')
    prev='base'
    for i,(_,start,end) in enumerate(crops):
        out=f'layer{i}'
        parts.append(f"[{prev}][zoom{i}]overlay={place.x}:{place.y}:enable='gte(t,{start})*lt(t,{end})':shortest=1[{out}]")
        prev=out
    parts.append("[layer2]drawbox=x=86:y=506:w=908:h=854:color=0x4EE0C5:t=4:enable='gte(t,8.4)*lt(t,17.2)'[out]")
    return ';'.join(parts)
