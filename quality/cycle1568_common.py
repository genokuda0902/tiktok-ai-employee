"""Reusable 10-genre timing and fictional-data validation for review videos."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    title: str
    subtitle: str
    seconds: float = 3.0

def validate(scenes, fps=24, width=1080, height=1920):
    if not scenes or len(scenes) > 12:
        raise ValueError("1-12 scenes required")
    if fps < 24 or width < 720 or height < 1280 or width * 16 != height * 9:
        raise ValueError("invalid vertical output")
    for scene in scenes:
        if not scene.title.strip() or not scene.subtitle.strip() or scene.seconds <= 0:
            raise ValueError("incomplete scene")
    return sum(scene.seconds for scene in scenes)

def progress_frame(t, duration, width=900):
    if duration <= 0:
        raise ValueError("duration")
    return round(width * min(1, max(0, t / duration)))

def publication_gate(narration_verified=False, sync_verified=False, rights_approved=False, human_approved=False):
    return all((narration_verified, sync_verified, rights_approved, human_approved))
