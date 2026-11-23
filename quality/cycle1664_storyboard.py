"""Ten-genre reusable storyboard timing and publication gate. Review-only."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    headline: str
    subtitle: str

def validate(scenes, duration, *, japanese_narration=False, sync_verified=False, asset_approved=False, employee_approved=False):
    issues = []
    if not scenes: issues.append("missing_scenes")
    cursor = 0.0
    for scene in scenes:
        if scene.start < cursor - 0.01 or scene.end <= scene.start or scene.end > duration + 0.01:
            issues.append("invalid_timing")
        if not scene.headline.strip() or not scene.subtitle.strip():
            issues.append("missing_text")
        if len(scene.subtitle) > 32:
            issues.append("subtitle_too_long")
        cursor = scene.end
    if scenes and abs(cursor-duration)>0.1: issues.append("duration_gap")
    if not japanese_narration: issues.append("missing_japanese_narration")
    if not sync_verified: issues.append("unverified_caption_sync")
    if not asset_approved: issues.append("unapproved_asset")
    if not employee_approved: issues.append("employee_review_required")
    return sorted(set(issues))
