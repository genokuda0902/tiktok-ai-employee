"""Reusable 10-genre storyboard validation; review-only by default."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    duration: float
    headline: str
    visual: str

def validate_storyboard(scenes, narration_verified=False, captions_synced=False, employee_approved=False):
    errors = []
    if not scenes or len(scenes) < 3: errors.append("at_least_three_scenes")
    if any(s.duration <= 0 or not s.headline.strip() or not s.visual.strip() for s in scenes):
        errors.append("invalid_scene")
    if scenes and not (6 <= sum(s.duration for s in scenes) <= 45):
        errors.append("duration_out_of_range")
    if not narration_verified: errors.append("japanese_narration_unverified")
    if not captions_synced: errors.append("speech_caption_sync_unverified")
    if not employee_approved: errors.append("employee_approval_missing")
    return {"posting_allowed": not errors, "issues": errors, "status": "APPROVED" if not errors else "PUBLICATION_NOT_APPROVED"}
