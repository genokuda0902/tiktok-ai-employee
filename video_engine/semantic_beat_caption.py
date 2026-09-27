"""Semantic beat captions for zero-cost image-slide videos.

Keeps viewer-facing text concise and maps each caption to a story beat.
No posting or paid service integration.
"""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Beat:
    start: float
    end: float
    text: str

def validate_beats(beats: Sequence[Beat], duration: float, width=1080, height=1920) -> bool:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if duration <= 0 or not beats:
        raise ValueError("positive duration and beats required")
    previous = 0.0
    for beat in beats:
        if not beat.text.strip() or len(beat.text.strip()) > 18:
            raise ValueError("beat copy must be a short readable phrase")
        if beat.start < previous or beat.end <= beat.start or beat.end > duration + 1e-6:
            raise ValueError("invalid beat timeline")
        previous = beat.end
    return True

def release_contract():
    return {
        "zero_cost": True,
        "semantic_caption_beats": True,
        "portrait_delivery": (1080, 1920),
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
