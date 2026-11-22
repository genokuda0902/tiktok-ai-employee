"""Shared storyboard quality gate for ten content genres. REVIEW ONLY."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Review:
    scene_count: int
    duration_seconds: float
    width: int
    height: int
    has_japanese_narration: bool
    captions_synchronized: bool
    approved_assets: bool
    employee_approved: bool

def issues(r: Review) -> list[str]:
    failures = []
    if r.scene_count < 3 or not 15 <= r.duration_seconds <= 60:
        failures.append("storyboard")
    if (r.width, r.height) != (1080, 1920):
        failures.append("vertical_resolution")
    if not r.has_japanese_narration:
        failures.append("japanese_narration")
    if not r.captions_synchronized:
        failures.append("caption_sync")
    if not r.approved_assets:
        failures.append("asset_approval")
    if not r.employee_approved:
        failures.append("employee_approval")
    return failures

def publishable(r: Review) -> bool:
    return not issues(r)
