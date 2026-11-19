"""Review-only frame/scene validator shared by ten genres. No publication approval implied."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    heading: str

def validate_scenes(scenes, duration):
    if not scenes or duration <= 0:
        raise ValueError("missing scenes or invalid duration")
    previous = 0.0
    for scene in scenes:
        if abs(scene.start - previous) > 0.001 or scene.end <= scene.start:
            raise ValueError("scene gap, overlap, or invalid duration")
        if not scene.heading.strip():
            raise ValueError("empty scene heading")
        previous = scene.end
    if abs(previous - duration) > 0.001:
        raise ValueError("total duration mismatch")
    return True

def publication_allowed(*, narration_verified=False, captions_synced=False,
                        assets_approved=False, employee_approved=False):
    return all((narration_verified, captions_synced, assets_approved, employee_approved))
