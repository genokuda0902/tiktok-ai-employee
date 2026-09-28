"""Single-source contract for the image-first TikTok production route.

Reimplementation: one manifest owns image copy, narration, phrase captions and timing.
No posting or paid service integration is performed here.
"""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class StoryCut:
    image_prompt: str
    image_copy: str
    narration: str
    caption: str
    duration: float

@dataclass(frozen=True)
class StoryManifest:
    genre: str
    cuts: Sequence[StoryCut]
    width: int = 1080
    height: int = 1920
    human_approval_required: bool = True
    manual_post_only: bool = True

    def validate(self) -> None:
        if (self.width, self.height) != (1080, 1920):
            raise ValueError("portrait delivery must be 1080x1920")
        if not 8 <= len(self.cuts) <= 12:
            raise ValueError("image-first stories require 8-12 cuts")
        if not self.human_approval_required or not self.manual_post_only:
            raise ValueError("human approval/manual posting are mandatory")
        for i, cut in enumerate(self.cuts):
            if not all((cut.image_prompt.strip(), cut.image_copy.strip(), cut.narration.strip(), cut.caption.strip())):
                raise ValueError(f"cut {i} has missing single-source content")
            if not 0.8 <= cut.duration <= 4.0:
                raise ValueError(f"cut {i} duration outside readable range")
            # Captions must be a phrase taken from the narration so copy cannot silently drift.
            normalized_narration = "".join(cut.narration.split())
            normalized_caption = "".join(cut.caption.split())
            if normalized_caption not in normalized_narration:
                raise ValueError(f"cut {i} caption drifts from narration")

    @property
    def duration(self) -> float:
        self.validate()
        return round(sum(c.duration for c in self.cuts), 3)


def release_contract() -> dict:
    return {
        "zero_cost": True,
        "image_first": True,
        "single_source_manifest": True,
        "cuts_min": 8,
        "cuts_max": 12,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
