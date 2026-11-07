"""Fail-closed review gate for image-first TikTok MP4 outputs.

No publication without explicit human approval and verified narration.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Review:
    width: int
    height: int
    duration: float
    video_decodes: bool
    japanese_narration_verified: bool
    captions_synced: bool
    rights_approved: bool
    employee_approved: bool

def publication_allowed(review: Review) -> bool:
    return all((
        review.width == 1080,
        review.height == 1920,
        8 <= review.duration <= 60,
        review.video_decodes,
        review.japanese_narration_verified,
        review.captions_synced,
        review.rights_approved,
        review.employee_approved,
    ))
