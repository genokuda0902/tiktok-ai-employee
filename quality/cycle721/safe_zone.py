"""Reusable 1080x1920 TikTok safe-area Japanese caption layout.

This module is stdlib-only. It does not guarantee placement in every TikTok UI,
and makes no claims of forced speech alignment.
"""
from dataclasses import dataclass

VIDEO_W = 1080
VIDEO_H = 1920
FPS = 30
RIGHT_UI_EXCLUSION = 180
BOTTOM_UI_EXCLUSION = 315

GENRE_COLORS = {
    "AI・仕事効率化": "#61D6FF",
    "美容・身だしなみ": "#FFB3CE",
    "恋愛・心理": "#ED9BFF",
    "お金・節約": "#78E4B2",
    "営業・ビジネス": "#FFC86A",
    "転職・キャリア": "#A9C1FF",
    "健康・生活改善": "#83E0C9",
    "雑学・科学": "#42E5D0",
    "旅行・グルメ": "#FFA785",
    "商品比較・暮らし": "#D0DCA5",
}

@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h

CAPTION_CARD = Rect(56, 1398, 840, 202)

def is_inside_assumed_safe_zone(rect=CAPTION_CARD):
    return (rect.x >= 0 and rect.y >= 0
            and rect.right <= VIDEO_W - RIGHT_UI_EXCLUSION
            and rect.bottom <= VIDEO_H - BOTTOM_UI_EXCLUSION)

def validate_cues(cues, expected_scenes=8):
    if len(cues) != expected_scenes:
        raise ValueError("unexpected scene count")
    for i, cue in enumerate(cues):
        if len(cue["phrases"]) != 2 or not all(cue["phrases"]):
            raise ValueError("expected two nonempty Japanese phrases")
        if not cue["start_s"] < cue["boundary_s"] < cue["end_s"]:
            raise ValueError("invalid phrase timing")
        if i and abs(cue["start_s"] - cues[i-1]["end_s"]) > 0.002:
            raise ValueError("caption timing gap")
    return True

def validate_genre(genre):
    if genre not in GENRE_COLORS:
        raise ValueError("unknown genre")
    return GENRE_COLORS[genre]
