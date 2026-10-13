"""Reusable 10-genre subject-only parallax configuration; no paid API or posting."""
from math import cos, pi
GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)
FPS = 30
SCENE_BOUNDARIES = (0, 53, 106, 165, 196, 230, 284, 335, 375)
SCENE_FRAMES = tuple(b - a for a, b in zip(SCENE_BOUNDARIES[:-1], SCENE_BOUNDARIES[1:]))
DIRECTIONS = ((20,-8),(-20,10),(18,-12),(-22,8),(24,-8),(-18,12))
def ease_cos(progress):
    t = max(0.0, min(1.0, float(progress)))
    return (1 - cos(pi*t))/2
def subject_offset(scene_index, progress):
    if scene_index not in range(2,8):
        raise ValueError("scene_index must be 2..7")
    dx, dy = DIRECTIONS[scene_index - 2]
    e = ease_cos(progress)
    return -22 + dx*e, -38 + dy*e
def ffmpeg_motion(scene_index):
    if scene_index not in range(2,8):
        raise ValueError("scene_index must be 2..7")
    dx, dy = DIRECTIONS[scene_index - 2]
    duration = SCENE_FRAMES[scene_index]/FPS
    ease = f"(1-cos(PI*t/{duration:.7f}))/2"
    return f"-22+({dx})*{ease}", f"-38+({dy})*{ease}"
