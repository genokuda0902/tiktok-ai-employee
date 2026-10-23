"""cycle797: image-stage and inherited Japanese subtitle alignment contract.

Only metadata and tests are committed; source voice and AI imagery require
human rights review. No automatic publication or unapproved media upload.
"""
from bisect import bisect_right

WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENE_FRAMES = (57, 63, 58, 63, 40, 47, 48, 53)
ART_RECT = (35, 430, 1010, 1050)
SUBTITLE_SAFE_RECT = (30, 1530, 1020, 230)
GENRES = {
    "ai_work": "#9B90FF", "beauty": "#E5ACD7",
    "love_psychology": "#C0A2FF", "money_saving": "#6BE1B8",
    "sales_business": "#58C5F6", "career": "#83C5F9",
    "health_life": "#6EE7BE", "science": "#39E7D3",
    "travel_food": "#70D6EA", "product_life": "#C6A0F5",
}
# Index corresponds to the narration's existing 8-scene timeline.
SCENES = (
    ("この基板、", "実はパソコン", "Raspberry Pi"),
    ("手のひらサイズ、", "でも本格派", "Raspberry Pi"),
    ("画面につなげば、", "操作できる", "HDMI / display"),
    ("必要なのは、", "三つの接続", "power / display / input"),
    ("まずは", "三つをつなぐ", "power / display / input"),
    ("入力・処理・", "出力", "input / process / output"),
    ("最初は、", "たった一行", "Python first line"),
    ("保存して、", "あとで試そう", "save"),
)

def scene_index(frame):
    if not 0 <= frame < sum(SCENE_FRAMES):
        raise ValueError("Frame outside timeline")
    totals = []
    s = 0
    for duration in SCENE_FRAMES:
        s += duration
        totals.append(s)
    return bisect_right(totals, frame)

def validate():
    assert len(GENRES) == 10
    assert len(SCENES) == 8
    assert sum(SCENE_FRAMES) == 429
    x, y, w, h = ART_RECT
    sx, sy, sw, sh = SUBTITLE_SAFE_RECT
    assert 0 <= x and 0 <= y and x + w <= WIDTH and y + h <= HEIGHT
    assert y + h <= sy
    assert sx >= 0 and sy >= 0 and sx + sw <= WIDTH and sy + sh <= HEIGHT
    assert all(len(color) == 7 and color.startswith("#") for color in GENRES.values())
    return True
