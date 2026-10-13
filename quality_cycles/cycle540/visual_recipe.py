"""Cycle540 reusable, original, review-only slide recipe (no paid services)."""
from dataclasses import dataclass
from typing import Tuple

GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理",
    "お金・節約", "営業・ビジネス", "転職・キャリア",
    "健康・生活改善", "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)
SCENE_VISUALS = (
    "macro_pcb", "macro_pcb", "monitor_dashboard", "code_editor",
    "breadboard_circuit", "automation_flow", "robot_arm", "bookmark",
)
CUTS = (0.0, 1.77, 3.52, 5.50, 6.55, 7.66, 9.48, 11.18, 12.50)
WIDTH, HEIGHT, FPS = 1080, 1920, 30

@dataclass(frozen=True)
class ReviewPolicy:
    rights: str = "original procedural imagery; reused authorized voice"
    publication: str = "NOT_APPROVED"
    human_review: str = "PENDING"
    auto_post: bool = False

def scene_at(time_s: float) -> int:
    """Return scene index for a valid video timestamp."""
    if not 0 <= time_s < CUTS[-1]:
        raise ValueError("timestamp outside video")
    return next(i for i in range(8) if CUTS[i] <= time_s < CUTS[i + 1])

def subject_zone() -> Tuple[int, int]:
    """The six new subject illustrations avoid the burned-in caption region."""
    return 545, 1375

def validate_layout(width=WIDTH, height=HEIGHT, fps=FPS):
    if (width, height, fps) != (1080, 1920, 30):
        raise ValueError("TikTok output must be 1080x1920 at 30fps")
    if not (subject_zone()[1] < 1430):
        raise ValueError("subject art overlaps Japanese subtitle safe zone")
    return True

def assert_review_only(policy=ReviewPolicy()):
    if policy.auto_post or policy.publication != "NOT_APPROVED":
        raise ValueError("Human approval and manual posting are mandatory")
    return True
