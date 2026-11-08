"""Fail-closed review gate for 10 genre-agnostic video pipelines."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    width: int
    height: int
    video_decodes: bool
    japanese_narration_verified: bool
    speech_captions_aligned: bool
    assets_approved: bool
    privacy_review_passed: bool
    employee_approved: bool

def assess(e: Evidence) -> dict:
    checks = {
        "1080p_vertical": e.width >= 1080 and e.height >= 1920,
        "decodes": e.video_decodes,
        "japanese_narration": e.japanese_narration_verified,
        "speech_captions": e.speech_captions_aligned,
        "assets_approved": e.assets_approved,
        "privacy": e.privacy_review_passed,
        "employee_approval": e.employee_approved,
    }
    return {"checks": checks, "posting_allowed": all(checks.values()),
            "status": "APPROVED_FOR_MANUAL_POST" if all(checks.values()) else "REVIEW_ONLY"}
