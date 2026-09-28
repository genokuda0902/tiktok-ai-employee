"""Zero-cost scene-level caption overlay for semantic image slides.

Captions are rendered separately from source images so text can change with each
semantic beat without baking copy into the image asset. This module does not post.
"""
from dataclasses import dataclass

REQUIRED_BEATS = ("hook", "problem", "solution", "demo", "result", "cta")

@dataclass(frozen=True)
class CaptionCue:
    beat: str
    start_s: float
    end_s: float
    text: str


def validate_cues(cues: list[CaptionCue], width: int = 1080, height: int = 1920) -> None:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if len(cues) != 6 or tuple(c.beat for c in cues) != REQUIRED_BEATS:
        raise ValueError("six semantic caption cues are required in canonical order")
    previous_end = 0.0
    for cue in cues:
        if not cue.text.strip() or cue.start_s < 0 or cue.end_s <= cue.start_s:
            raise ValueError("caption cue is invalid")
        if abs(cue.start_s - previous_end) > 0.04:
            raise ValueError("caption cues must be contiguous")
        previous_end = cue.end_s


def render_policy() -> dict:
    return {
        "zero_cost": True,
        "caption_layer_separate_from_image": True,
        "japanese_font_required": True,
        "human_quality_review_required": True,
        "human_rights_review_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
