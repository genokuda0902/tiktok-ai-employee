"""Phrase-level caption schedule for image-first TikTok stories.

Keeps captions short and timed, while preserving the repository's human-approval
and manual-post-only safety contract. Zero-cost and genre-independent.
"""
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class CaptionCue:
    start: float
    end: float
    text: str

    def validate(self) -> None:
        if self.start < 0 or self.end <= self.start:
            raise ValueError("caption cue requires positive ordered timing")
        if not self.text.strip():
            raise ValueError("caption cue text is required")
        if len(self.text.strip()) > 32:
            raise ValueError("caption cue must remain phrase-sized (<=32 chars)")


def validate_caption_track(
    cues: Sequence[CaptionCue],
    *,
    video_duration: float,
    human_approval_required: bool = True,
    manual_post_only: bool = True,
) -> None:
    if not human_approval_required or not manual_post_only:
        raise ValueError("human approval/manual posting are mandatory")
    if video_duration <= 0:
        raise ValueError("video_duration must be positive")
    previous_end = 0.0
    for cue in cues:
        cue.validate()
        if cue.start < previous_end:
            raise ValueError("caption cues must not overlap")
        if cue.end > video_duration + 0.05:
            raise ValueError("caption cue exceeds video duration")
        previous_end = cue.end
