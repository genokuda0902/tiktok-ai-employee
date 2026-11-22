"""Review-only scene timing checks, reusable across content genres."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    duration: float
    title: str
    caption: str

def validate_scenes(scenes, audio_verified=False, rights_approved=False, human_approved=False):
    if not scenes or any(s.duration <= 0 or not s.title.strip() or not s.caption.strip() for s in scenes):
        raise ValueError("Every scene needs positive duration, title and caption")
    timeline = []
    cursor = 0.0
    for scene in scenes:
        timeline.append({"start": round(cursor, 3), "end": round(cursor + scene.duration, 3), "caption": scene.caption})
        cursor += scene.duration
    return {"timeline": timeline, "duration": round(cursor, 3), "posting_allowed": bool(audio_verified and rights_approved and human_approved), "quality_status": "REVIEW_ONLY"}
