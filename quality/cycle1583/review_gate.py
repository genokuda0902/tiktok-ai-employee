"""Fail-closed review checks for all ten TikTok genres (cycle1583)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReviewEvidence:
    video_stream: bool
    japanese_voice_verified: bool
    caption_timing_verified: bool
    safe_area_verified: bool
    asset_rights_verified: bool
    privacy_reviewed: bool
    employee_approved: bool

def publication_issues(e: ReviewEvidence) -> list[str]:
    return [name for name in ReviewEvidence.__dataclass_fields__
            if not getattr(e, name)]

def may_publish(e: ReviewEvidence) -> bool:
    return not publication_issues(e)
