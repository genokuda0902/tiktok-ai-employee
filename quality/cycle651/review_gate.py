"""Cycle651: reusable fail-closed review gate for ten TikTok genres.

This file does not approve rights, voices, posting, or publication.
"""
from dataclasses import dataclass

GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)

@dataclass(frozen=True)
class ReviewPolicy:
    publication: str = "NOT_APPROVED"
    asset_rights: str = "UNVERIFIED"
    narration_status: str = "ABSENT"
    posting: str = "MANUAL_AFTER_APPROVAL"

def validate_review_plan(plan):
    """Validate a review-only 20s, eight-scene, 9:16 proof video plan."""
    if plan.get("genre") not in GENRES:
        raise ValueError("unknown genre")
    for key, expected in vars(ReviewPolicy()).items():
        if plan.get(key) != expected:
            raise ValueError(f"{key} must be {expected}; publication blocked")
    data = plan.get("data")
    if not isinstance(data, list) or len(data) != 4 or sum(data) != 650:
        raise ValueError("synthetic proof data mismatch")
    scenes = plan.get("scenes", [])
    if len(scenes) != 8:
        raise ValueError("eight scenes required")
    if abs(scenes[0]["start"]) > .001 or abs(scenes[-1]["end"] - 20) > .001:
        raise ValueError("timeline must be exactly 20s")
    for i, s in enumerate(scenes):
        if not 1.3 <= s["end"] - s["start"] <= 3.1:
            raise ValueError("scene length invalid")
        if len(s.get("caption", "")) > 25:
            raise ValueError("caption too long")
        if i and abs(scenes[i-1]["end"] - s["start"]) > .001:
            raise ValueError("timeline gap/overlap")
    return True
