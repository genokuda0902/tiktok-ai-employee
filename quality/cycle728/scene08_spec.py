"""Shared, zero-cost, review-only scene 08 layout spec for 10 TikTok genres.

Actual video encoder and complete render/test bundle: cycle728 ZIP attachment.
This module is pure Python stdlib so CI can check timing and safe regions.
"""
from __future__ import annotations

WIDTH, HEIGHT, FPS = 1080, 1920, 30
START_FRAME, END_FRAME = 531, 605
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
SAFE = {"left": 48, "right": 900, "top": 58, "bottom": 1605}
STEPS = [
    ("01", "電源をつなぐ", "まずは起動の準備"),
    ("02", "画面と入力機器を用意", "操作できる環境をつくる"),
    ("03", "1行だけ実行する", "print(2 + 3) から始める"),
]
CAPTIONS = [
    (17.90, 18.4333, "保存して、"),
    (18.4333, 19.4667, "あとで試そう。"),
]

def layout():
    return {
        "header": (56, 65, 885, 172),
        "headline": (70, 260, 885, 455),
        "steps": [(64, 570 + i * 182, 888, 734 + i * 182) for i in range(3)],
        "caption": (65, 1246, 885, 1465),
    }

def caption_at(seconds):
    for start, end, phrase in CAPTIONS:
        if start <= seconds < end:
            return phrase
    return ""

def smooth(v):
    v = min(1.0, max(0.0, v))
    return v * v * (3 - 2 * v)

def validate():
    assert (WIDTH, HEIGHT, FPS) == (1080, 1920, 30)
    assert len(GENRES) == 10
    assert END_FRAME - START_FRAME == 74
    boxes = layout()
    for box in [boxes["header"], boxes["headline"], boxes["caption"], *boxes["steps"]]:
        x0, y0, x1, y1 = box
        assert SAFE["left"] <= x0 < x1 <= SAFE["right"]
        assert SAFE["top"] <= y0 < y1 <= SAFE["bottom"]
    assert all(box[3] < boxes["caption"][1] for box in boxes["steps"])
    assert CAPTIONS[0][1] == CAPTIONS[1][0]
    assert CAPTIONS[-1][1] < END_FRAME / FPS
    return True

if __name__ == "__main__":
    assert validate()
    print("cycle728 scene08 specification: PASS")
