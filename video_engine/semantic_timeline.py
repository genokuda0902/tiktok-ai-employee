"""Genre-independent semantic timeline for image-slide + Japanese narration + captions.

One scene owns one image interval, one narration interval, and one caption interval.
The contract prevents long unexplained gaps and can be reused across all content genres.
Human quality/rights approval and manual posting remain mandatory.
"""
from dataclasses import dataclass

MAX_GAP_S = 0.35

@dataclass(frozen=True)
class Scene:
    image: str
    narration: str
    caption: str
    duration_s: float


def validate_scenes(scenes: list[Scene]) -> float:
    if not scenes:
        raise ValueError("at least one scene is required")
    total = 0.0
    for i, s in enumerate(scenes):
        if not s.image or not s.narration.strip() or not s.caption.strip():
            raise ValueError(f"scene {i} must contain image, narration, and caption")
        if s.duration_s <= MAX_GAP_S:
            raise ValueError(f"scene {i} duration is too short for semantic delivery")
        total += s.duration_s
    return round(total, 3)


def build_timeline(scenes: list[Scene]) -> list[dict]:
    validate_scenes(scenes)
    out = []
    t = 0.0
    for i, s in enumerate(scenes):
        start = round(t, 3)
        end = round(t + s.duration_s, 3)
        out.append({
            "scene": i + 1,
            "start": start,
            "end": end,
            "image": s.image,
            "narration": s.narration,
            "caption": s.caption,
            "max_internal_gap_s": MAX_GAP_S,
        })
        t = end
    return out


def posting_policy() -> dict:
    return {"zero_cost": True, "human_approval_required": True, "auto_post": False}
