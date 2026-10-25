"""cycle854 reusable native-resolution Japanese editorial slide rules.

Review-only: 1080x1920 slide pixels do NOT imply native-resolution photographs.
The photo foreground is capped at 1.12x source resolution. No posting.
"""
from __future__ import annotations

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
PHOTO_MAX_SCALE = 1.12
SAFE_LEFT, SAFE_RIGHT, SAFE_TOP, SAFE_BOTTOM = 72, 910, 125, 1630
GENRES = {
    "ai_work": ("#101B2C", "#54F0D4"),
    "sales_business": ("#211E2B", "#FFBD71"),
    "beauty": ("#302234", "#F4A6D3"),
    "romance": ("#362232", "#F9A3C0"),
    "saving": ("#172B26", "#A4E6B0"),
    "career": ("#21283A", "#FFB49B"),
    "wellness": ("#243125", "#B9E99D"),
    "science": ("#182B42", "#91D0F8"),
    "travel_food": ("#183438", "#74DFE1"),
    "product_comparison_lifestyle": ("#2F2439", "#D7B0F7"),
}

def foreground_scale(w: int, h: int, box=(870, 575)) -> float:
    if min(w, h, *box) <= 0:
        raise ValueError("positive dimensions required")
    return min(box[0] / w, box[1] / h, PHOTO_MAX_SCALE)

def validate_beats(beats: list[dict]) -> bool:
    if len(beats) != 24:
        raise ValueError("24 Japanese narration beats required")
    previous_end = 0.0
    for beat in beats:
        start, end = float(beat["start"]), float(beat["end"])
        if start < previous_end or end <= start or end > FRAMES/FPS + 0.001:
            raise ValueError("invalid beat timeline")
        previous_end = end
    return True

def scene_count() -> int:
    return 8

def slide_dimensions() -> tuple[int,int]:
    return WIDTH, HEIGHT

def safe_width() -> int:
    return SAFE_RIGHT - SAFE_LEFT

def contrast_ratio(a: tuple[int,int,int], b: tuple[int,int,int]) -> float:
    def lum(c):
        def channel(v):
            v = v / 255
            return v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4
        return sum(weight*channel(v) for weight,v in zip((0.2126,0.7152,0.0722),c))
    hi,lo = sorted((lum(a),lum(b)), reverse=True)
    return (hi+0.05)/(lo+0.05)
