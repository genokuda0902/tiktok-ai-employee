"""Review-only subtitle layout checks shared by all content genres.

No speech synthesis is claimed. Fail closed for publication.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str

def validate_cues(cues, duration, frame_height=1920, top=1370, bottom=1580):
    if not cues or not (0 <= top < bottom <= frame_height - 240):
        raise ValueError("unsafe subtitle area")
    last = 0.0
    for cue in cues:
        if not (last <= cue.start < cue.end <= duration) or not cue.text.strip():
            raise ValueError("invalid or overlapping cue")
        last = cue.end
    return True

def publication_allowed(*, japanese_speech_verified=False, sync_verified=False,
                        asset_approved=False, employee_approved=False):
    return all((japanese_speech_verified, sync_verified, asset_approved, employee_approved))
