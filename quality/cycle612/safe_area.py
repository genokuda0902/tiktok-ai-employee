"""cycle612: original end-card safe-area configuration and 10-genre color palette.
Full MP4 renderer and inherited source media are supplied in the cycle612 ZIP.
This module intentionally contains no upload or publication code.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class SafeArea:
    x: int = 70
    y: int = 900
    width: int = 760
    height: int = 350
    canvas_width: int = 1080
    canvas_height: int = 1920
    final_scene_start: int = 415
    total_frames: int = 468

    def valid(self) -> bool:
        return (
            self.x >= 0 and self.y >= 700
            and self.x + self.width <= 850
            and self.y + self.height < 1320
            and self.final_scene_start == 415
            and self.total_frames == 468
        )

TEN_GENRES = {
    "AI・仕事効率化": "#39e6cc",
    "美容・身だしなみ": "#e9b6cb",
    "恋愛・心理": "#f0a2a2",
    "お金・節約": "#d6dd80",
    "営業・ビジネス": "#5bcce0",
    "転職・キャリア": "#c0b1ff",
    "健康・生活改善": "#8bd1a8",
    "雑学・科学": "#55ebc8",
    "旅行・グルメ": "#f2c88d",
    "商品比較・暮らし": "#94c6f7",
}

PUBLICATION_STATUS = "NOT_APPROVED"
QUALITY_STATUS = "HUMAN_REVIEW"
