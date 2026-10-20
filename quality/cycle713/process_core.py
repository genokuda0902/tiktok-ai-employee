"""Reusable process-stage and palette logic for cycle713. No external assets."""
from __future__ import annotations
SCENE_SECONDS = 1.95
SCENE_INDEX = 5
SCENE_START = SCENE_INDEX * SCENE_SECONDS
GENRE_COLORS = {
    "ai_work": "#54DAFF",
    "beauty": "#FF92D3",
    "love_psychology": "#EEA0F8",
    "saving": "#A8EA80",
    "sales_business": "#FFD36B",
    "career": "#C0A6FF",
    "health": "#80E6BC",
    "science": "#4FE2D2",
    "travel_food": "#FFB078",
    "product_comparison": "#7EC9FF",
}
STAGES = (
    ("入力", "2 + 3", "① 数字「2」と「3」を受け取る"),
    ("処理", "CPU", "② CPUが「2 + 3」を計算する"),
    ("出力", "5", "③ 結果の「5」を画面に表示"),
)
def stage_at(progress: float) -> int:
    if not 0 <= progress <= 1:
        raise ValueError("progress must be in [0,1]")
    return min(2, int(progress * 3))
def accent(genre: str) -> str:
    return GENRE_COLORS[genre]
def caption(progress: float) -> str:
    return STAGES[stage_at(progress)][2]
def stage_seconds(stage: int) -> tuple[float,float]:
    if stage not in (0,1,2):
        raise ValueError("stage out of bounds")
    return (SCENE_START + stage * SCENE_SECONDS/3,
            SCENE_START + (stage+1) * SCENE_SECONDS/3)
