"""cycle801 shared layout contract for image-first TikTok videos.
This module is media-agnostic; the full local review renderer and inherited
media are in the separately delivered review ZIP, not in this repository.
"""
from dataclasses import dataclass

WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENES = 8
CAPTION_BAND = (45, 1468, 1035, 1750)
IMAGE_CARD = (58, 367, 1022, 1417)
PALETTE = {
    "ai_work": "#B9A4FF",
    "beauty": "#FFB9DF",
    "love_psychology": "#D7B5FF",
    "money_saving": "#89EFCB",
    "sales_business": "#7FD7FF",
    "career": "#A4D8FF",
    "health_life": "#8AF0D1",
    "science": "#43E5D0",
    "travel_food": "#87E1F2",
    "product_life": "#D4B6FF",
}
HEADLINES = (
    "この小さな基板の正体", "手のひらに収まる", "画面につなぐ", "必要な3つの接続",
    "LEDを光らせる", "コンピューターの基本", "プログラムは1行から", "まず保存してみよう",
)

def scene_index(frame: int, total_frames: int = 429) -> int:
    if total_frames <= 0 or not (0 <= frame < total_frames):
        raise ValueError("invalid frame")
    return min(SCENES - 1, frame * SCENES // total_frames)

def validate_cues(cues: list[dict], total_frames: int) -> bool:
    if not cues:
        raise ValueError("no subtitles")
    previous_end = 0
    for cue in cues:
        if set(cue) != {"start", "end", "text", "accent"}:
            raise ValueError("invalid subtitle schema")
        if not (isinstance(cue["start"], int) and isinstance(cue["end"], int)
                and previous_end <= cue["start"] < cue["end"] <= total_frames):
            raise ValueError("invalid timing")
        if not cue["text"] or cue["accent"] not in cue["text"]:
            raise ValueError("invalid emphasis")
        previous_end = cue["end"]
    return True

def validate_layout():
    x1, y1, x2, y2 = CAPTION_BAND
    ax1, ay1, ax2, ay2 = IMAGE_CARD
    assert 0 <= x1 < x2 <= WIDTH
    assert 0 <= ax1 < ax2 <= WIDTH
    assert 0 <= ay1 < ay2 < y1 < y2 <= HEIGHT
    assert len(PALETTE) == 10 and len(set(PALETTE.values())) == 10
    assert len(HEADLINES) == SCENES
    return True
