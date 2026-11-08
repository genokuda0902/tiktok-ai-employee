"""Fail-closed, genre-independent scene/caption timeline validation."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    caption: str

def validate_timeline(scenes, duration, narration_verified=False, rights_approved=False, human_approved=False):
    errors = []
    if not scenes:
        errors.append("no_scenes")
    previous = 0.0
    for scene in scenes:
        if scene.start < 0 or scene.end <= scene.start or scene.end > duration:
            errors.append("invalid_interval")
        if abs(scene.start - previous) > 0.05:
            errors.append("gap_or_overlap")
        if not scene.caption.strip():
            errors.append("missing_caption")
        previous = scene.end
    if scenes and abs(previous-duration) > 0.05:
        errors.append("duration_mismatch")
    if not narration_verified:
        errors.append("narration_unverified")
    if not rights_approved:
        errors.append("rights_unapproved")
    if not human_approved:
        errors.append("human_unapproved")
    return sorted(set(errors))
