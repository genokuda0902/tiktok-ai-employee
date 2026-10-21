"""cycle732 desktop-slide reusable design contract. All art is procedural."""
from dataclasses import dataclass
FPS = 30
WIDTH, HEIGHT = 1080, 1920
START, END = 163, 245
GENRES = {
    "AI・仕事効率化": "#5DD9FF",
    "美容・身だしなみ": "#FFB2D3",
    "恋愛・心理": "#DCA9FF",
    "お金・節約": "#81E4B2",
    "営業・ビジネス": "#FFCC74",
    "転職・キャリア": "#ADC6FF",
    "健康・生活改善": "#7DDFCA",
    "雑学・科学": "#56E6D4",
    "旅行・グルメ": "#FFAD8C",
    "商品比較・暮らし": "#D7E6A3",
}
CAPTIONS = ((5.6667,6.6667,"画面につなげば、"),(6.6667,7.5,"操作できる。"))
SAFE_RIGHT, SAFE_BOTTOM = 900, 1600

def speech_caption(t):
    for start,end,text in CAPTIONS:
        if start <= t < end:
            return text
    return ""

def step(frame):
    if not START <= frame < END:
        raise ValueError("frame out of range")
    progress = (frame-START)/(END-START)
    return 0 if progress < .34 else 1 if progress < .68 else 2

def safe_caption_rect(rect):
    left,top,right,bottom = rect
    return 0 <= left < right <= SAFE_RIGHT and 0 <= top < bottom <= SAFE_BOTTOM

def validate():
    assert len(GENRES)==len(set(GENRES.values()))==10
    assert (WIDTH,HEIGHT,FPS)==(1080,1920,30)
    assert END-START==82
    assert safe_caption_rect((55,1401,895,1580))
    return True
