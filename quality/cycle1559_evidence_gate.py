"""Fail-closed review-only video evidence gate. No audio presence == speech proof."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    width: int
    height: int
    duration: float
    video_decodes: bool
    audio_stream: bool
    japanese_voice_verified: bool
    captions_synchronized: bool
    assets_approved: bool
    employee_approved: bool

def evaluate(e: Evidence) -> dict:
    issues = []
    if not e.video_decodes: issues.append("video_decode_failed")
    if e.width < 720 or e.height < 1280: issues.append("resolution_low")
    if not 15 <= e.duration <= 60: issues.append("duration_outside_review_range")
    if not e.audio_stream: issues.append("audio_missing")
    if not e.japanese_voice_verified: issues.append("japanese_narration_unverified")
    if not e.captions_synchronized: issues.append("caption_sync_unverified")
    if not e.assets_approved: issues.append("asset_rights_unverified")
    if not e.employee_approved: issues.append("employee_approval_missing")
    return {"posting_allowed": not issues, "issues": issues, "review_only": bool(issues)}
