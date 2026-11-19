"""Shared 10-genre animation timing and safe publishing gate. cycle1572."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    title: str
    subtitle: str
    start: float
    end: float

def validate_scenes(scenes, duration):
    if not scenes or duration <= 0:
        raise ValueError("missing scenes or invalid duration")
    cursor = 0.0
    for scene in scenes:
        if abs(scene.start - cursor) > 0.001 or scene.end <= scene.start:
            raise ValueError("non-contiguous or invalid scene timing")
        cursor = scene.end
    if abs(cursor - duration) > 0.001:
        raise ValueError("scene duration mismatch")
    return True

def publication_allowed(*, japanese_speech_verified, captions_synced,
                        rights_approved, employee_approved):
    return all((japanese_speech_verified, captions_synced,
                rights_approved, employee_approved))
