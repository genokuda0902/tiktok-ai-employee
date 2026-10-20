"""Reusable scene-4 connection sequence for 10 TikTok genres.

Companion full-resolution Pillow/FFmpeg renderer is included in the
cycle714 reproducible archive. Not approved for publication.
"""
from dataclasses import dataclass
GENRE_COLORS = {
    "ai_work":"#54DAFF", "beauty":"#FF92D3",
    "love_psychology":"#EEA0F8", "saving":"#A8EA80",
    "sales_business":"#FFD36B", "career":"#C0A6FF",
    "health":"#80E6BC", "science":"#4FE2D2",
    "travel_food":"#FFB078", "product_comparison":"#7EC9FF",
}
CONNECTIONS = (
    ("電源", "USB-C"),
    ("画面", "micro HDMI"),
    ("入力", "USB-A"),
)
WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENE_INDEX, SCENE_SECONDS, PANEL_FRAMES = 3, 1.95, 59
PANEL_RECT = (70, 540, 940, 700)
CAPTION_TOP = 1340
@dataclass(frozen=True)
class ConnectionStep:
    index: int
    title: str
    connector: str
    start_seconds: float

def stage(progress: float) -> int:
    if not 0 <= progress <= 1:
        raise ValueError("progress outside 0..1")
    return min(2, int(progress * 3))

def steps():
    return tuple(ConnectionStep(i, title, port,
        SCENE_INDEX * SCENE_SECONDS + i * SCENE_SECONDS / 3)
        for i, (title, port) in enumerate(CONNECTIONS))

def validate(genre: str):
    if genre not in GENRE_COLORS:
        raise ValueError("unknown genre")
    x, y, w, h = PANEL_RECT
    assert WIDTH == 1080 and HEIGHT == 1920 and FPS == 30
    assert x >= 0 and y >= 0 and x + w <= WIDTH
    assert y + h < CAPTION_TOP
    assert len(CONNECTIONS) == 3
    return True
