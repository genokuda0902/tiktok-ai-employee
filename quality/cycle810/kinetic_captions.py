"""Cycle810: portable ten-genre Japanese subtitle timing engine.
No network calls, no publishing. Scene-relative timing is an estimate, not ASR alignment.
"""
from __future__ import annotations

FPS = 30
WIDTH = 1080
HEIGHT = 1920
AUTO_POST = False
EMPLOYEE_APPROVAL = False
GENRES = (
    "ai_work", "beauty", "love_psychology", "money_saving",
    "sales_business", "career", "health_life", "science",
    "travel_food", "product_life",
)
PALETTE = {
    "ai_work": "#56AFFF", "beauty": "#FF8BB7",
    "love_psychology": "#CA8AFF", "money_saving": "#78D9A8",
    "sales_business": "#46E2C5", "career": "#6DB4FF",
    "health_life": "#9AE27A", "science": "#6AD8FF",
    "travel_food": "#FFBB73", "product_life": "#A3A3FF",
}
CHUNKS = (
    ("仕事ができる人は、", "質問が", "違う。"),
    ("まず、", "目指すゴールを", "確認する。"),
    ("次に、", "今の数字を", "確かめる。"),
    ("そして、", "理想との差を", "一つに絞る。"),
    ("原因には、", "なぜを三回", "重ねる。"),
    ("対策は、", "今日できる行動に", "変える。"),
    ("結果を見て、", "また", "修正する。"),
    ("小さな改善が、", "強いチームを", "つくる。"),
)

def allocate_frames(total: int, chunks: tuple[str, ...] | list[str]) -> list[int]:
    """Exact integer frame budget, >=3 frames per highlighted chunk."""
    if total < len(chunks) * 3:
        raise ValueError("Scene too short for three-frame minimum")
    weights = [max(2, len(c.strip("、。！？"))) for c in chunks]
    remaining = total - len(chunks) * 3
    fractions = [remaining * w / sum(weights) for w in weights]
    result = [3 + int(x) for x in fractions]
    deficit = total - sum(result)
    order = sorted(range(len(chunks)), key=lambda i: fractions[i] - int(fractions[i]), reverse=True)
    for i in order[:deficit]:
        result[i] += 1
    assert sum(result) == total and min(result) >= 3
    return result

def build_timeline(scene_frames: list[int]) -> list[dict]:
    """Return 24 ordered phases and frame offsets; not forced alignment."""
    if len(scene_frames) != len(CHUNKS):
        raise ValueError("Expected eight scene durations")
    offset = 0
    result = []
    for i, (total, chunks) in enumerate(zip(scene_frames, CHUNKS)):
        for phase, length in enumerate(allocate_frames(total, chunks)):
            result.append({
                "scene": i + 1,
                "phase": phase + 1,
                "start_frame": offset,
                "frames": length,
                "highlight": chunks[phase],
                "full_subtitle": "".join(chunks),
            })
            offset += length
    return result

def validate_review_gate(genre: str, approved: bool = False) -> None:
    if genre not in GENRES:
        raise ValueError("Unsupported genre")
    if approved or AUTO_POST or EMPLOYEE_APPROVAL:
        raise PermissionError("Publication gate is intentionally closed")
