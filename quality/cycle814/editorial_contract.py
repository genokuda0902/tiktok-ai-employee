"""Reusable 10-genre 9:16 editorial card quality contract (stdlib only)."""
from __future__ import annotations

GENRE_ACCENTS = {
    "ai_work": "#77d5ff",
    "beauty": "#ffa2c3",
    "love_psychology": "#c3a0ff",
    "money_saving": "#ffd475",
    "sales_business": "#61f0c7",
    "career": "#84b9ff",
    "health_life": "#b4e97d",
    "science": "#86d9ff",
    "travel_food": "#ffbb8b",
    "product_life": "#d7b0ff",
}
WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAPTION_SAFE_ZONE = (72, 1360, 1008, 1618)
MIN_BOTTOM_UI_CLEARANCE = 250
SCENE_COUNT = 8
CAPTIONS = (
    "仕事ができる人は、質問が違う。",
    "まず、目指すゴールを確認する。",
    "次に、今の数字を確かめる。",
    "そして、理想との差を一つに絞る。",
    "原因には、なぜを三回重ねる。",
    "対策は、今日できる行動に変える。",
    "結果を見て、また修正する。",
    "小さな改善が、強いチームをつくる。",
)

def check_scene_contract(scenes, captions=CAPTIONS):
    """Validate structural properties without relying on unavailable licensed media."""
    assert len(GENRE_ACCENTS) == 10
    assert (WIDTH, HEIGHT, FPS) == (1080, 1920, 30)
    assert len(scenes) == SCENE_COUNT
    assert len(captions) == SCENE_COUNT
    assert all(isinstance(c, str) and c.strip() for c in captions)
    x0, y0, x1, y1 = CAPTION_SAFE_ZONE
    assert 0 <= x0 < x1 <= WIDTH
    assert 0 <= y0 < y1 <= HEIGHT - MIN_BOTTOM_UI_CLEARANCE
    return True

def validate_probe(probe):
    """Inspect ffprobe -show_streams JSON for technical video contract."""
    streams = probe["streams"]
    video = next(s for s in streams if s["codec_type"] == "video")
    audio = next(s for s in streams if s["codec_type"] == "audio")
    return {
        "1080x1920": (video["width"], video["height"]) == (WIDTH, HEIGHT),
        "h264_30fps": video["codec_name"] == "h264" and video["r_frame_rate"] == "30/1",
        "aac_48khz": audio["codec_name"] == "aac" and audio["sample_rate"] == "48000",
    }
