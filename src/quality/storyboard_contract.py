"""Genre-neutral storyboard QA. Review-only; never grants publication approval."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    caption: str

def validate(scenes, duration, *, japanese_audio_verified=False, human_approved=False):
    errors = []
    if not scenes: errors.append("missing_scenes")
    previous = 0.0
    for index, scene in enumerate(scenes):
        if scene.start < previous - 0.02: errors.append(f"overlap_or_disorder:{index}")
        if scene.end <= scene.start: errors.append(f"invalid_duration:{index}")
        if scene.end - scene.start < 1.0: errors.append(f"unreadable_timing:{index}")
        if not scene.caption.strip(): errors.append(f"empty_caption:{index}")
        if len(scene.caption) > 35: errors.append(f"long_caption:{index}")
        previous = scene.end
    if scenes and abs(previous - duration) > 0.05: errors.append("duration_mismatch")
    if not japanese_audio_verified: errors.append("japanese_narration_unverified")
    if not human_approved: errors.append("publication_not_approved")
    return errors
