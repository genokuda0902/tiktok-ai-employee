"""Cycle 686 reusable ten-genre subtitle contract. No posting, no TTS claim."""
from __future__ import annotations

PALETTES = {
    "ai_work": ("#40E2F2", "#91ABFF"),
    "beauty": ("#F78DD0", "#B0A1F7"),
    "love_psychology": ("#F5A7D1", "#A8CBF9"),
    "saving": ("#82E7A5", "#F3D083"),
    "sales_business": ("#57E7C0", "#F4C981"),
    "career": ("#89C3F5", "#80E1D0"),
    "health": ("#70E7B8", "#9BCDF3"),
    "science": ("#49EFD2", "#83B6FC"),
    "travel_food": ("#F3C475", "#82DCCE"),
    "product_comparison": ("#B6ABF8", "#85DBE5"),
}
SCRIPT_LINES = {
    1: ("これ、ただの基板じゃ", "ありません。"),
    2: ("小さくても、", "パソコンとして動きます。"),
    3: ("モニターにつなげば、", "画面で操作できます。"),
    4: ("電源と周辺機器を", "つないで、準備します。"),
    5: ("LEDを光らせる", "工作にも使えます。"),
    6: ("入力して、処理して、", "結果を出す。"),
    7: ("最初は、小さな作品から", "始めましょう。"),
}
WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAPTION_TOP, CAPTION_BOTTOM = 1360, 1667
STATUS = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"

def validate(timeline):
    """Require contiguous voiced scenes, script identity, safe area, no posting."""
    if len(timeline) != 8 or len(PALETTES) != 10:
        raise ValueError("expected eight scenes and ten genres")
    if CAPTION_BOTTOM > 1680 or (WIDTH, HEIGHT, FPS) != (1080, 1920, 30):
        raise ValueError("unsafe geometry")
    end = 0.0
    for n, item in enumerate(timeline, 1):
        if item["scene"] != n or abs(item["start"] - end) > 0.04:
            raise ValueError("scene gap/order")
        if item["end"] <= item["start"]:
            raise ValueError("nonpositive scene")
        if n <= 7 and "".join(SCRIPT_LINES[n]) != item["spoken_text"]:
            raise ValueError("script mismatch")
        if n == 8 and item["spoken_text"]:
            raise ValueError("silent CTA cannot contain speech")
        end = item["end"]
    if abs(end - 15.6) > .001:
        raise ValueError("duration mismatch")
    return True

def estimated_progress(scene, time_seconds, timeline):
    """Visual pacing estimate only, NOT acoustic forced alignment."""
    item = timeline[scene - 1]
    return max(0., min(1., (time_seconds - item["start"]) / (item["end"] - item["start"])))

def require_human_review(approved=False, auto_post=False):
    if approved or auto_post:
        raise ValueError("unapproved or automated publication forbidden")
    return STATUS
