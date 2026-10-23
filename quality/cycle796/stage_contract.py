"""Shared visual/QA contract for cycle796 (all 10 genres).

The actual Japanese-audio finished render is produced locally using a
review-only inherited MP4 and a separately generated image asset.
Neither unapproved media nor inherited narration is committed.
"""
from bisect import bisect_right

GENRE_THEMES = {
    "ai_work": "#9B90FF",
    "beauty": "#E5ACD7",
    "love_psychology": "#C0A2FF",
    "money_saving": "#6BE1B8",
    "sales_business": "#58C5F6",
    "career": "#83C5F9",
    "health_life": "#6EE7BE",
    "science": "#39E7D3",
    "travel_food": "#70D6EA",
    "product_life": "#C6A0F5",
}
SCENE_FRAMES = (57, 63, 58, 63, 40, 47, 48, 53)
WIDTH, HEIGHT, FPS = 1080, 1920, 30
ART_RECT = (35, 430, 1010, 1050)
SUBTITLE_SAFE_RECT = (30, 1530, 1020, 230)

def scene_index(frame: int, frames=SCENE_FRAMES) -> int:
    """Return 0-based scene number, avoiding rounding drift."""
    if frame < 0 or frame >= sum(frames):
        raise ValueError("Frame outside timeline")
    boundaries = []
    total = 0
    for duration in frames:
        total += duration
        boundaries.append(total)
    return bisect_right(boundaries, frame)

def validate_contract():
    assert len(GENRE_THEMES) == 10
    assert len(SCENE_FRAMES) == 8
    assert sum(SCENE_FRAMES) == 429
    x, y, w, h = ART_RECT
    sx, sy, sw, sh = SUBTITLE_SAFE_RECT
    assert 0 <= x < WIDTH and 0 <= y < HEIGHT
    assert x + w <= WIDTH and y + h <= HEIGHT
    assert y + h <= sy, "Artwork must not cover subtitles"
    assert sx >= 0 and sy + sh <= HEIGHT and sx + sw <= WIDTH
    assert all(color.startswith("#") and len(color) == 7 for color in GENRE_THEMES.values())
    return True

if __name__ == "__main__":
    validate_contract()
    print("cycle796: 10 genres, 8 scenes, safe area PASS")
