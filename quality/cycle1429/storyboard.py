"""Cross-genre story structure validation for review-only short videos."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Beat:
    role: str
    start: float
    end: float
    text: str

ROLES = ("hook", "demonstration", "verification")

def validate(beats, duration=15.0):
    if len(beats) != len(ROLES):
        raise ValueError("Exactly three narrative beats required")
    for i, (beat, role) in enumerate(zip(beats, ROLES)):
        if beat.role != role or not beat.text.strip():
            raise ValueError("Missing or misplaced narrative beat")
        if beat.end <= beat.start:
            raise ValueError("Non-positive beat duration")
        if i and abs(beat.start - beats[i-1].end) > 0.001:
            raise ValueError("Gap or overlap in timeline")
    if abs(beats[0].start) > 0.001 or abs(beats[-1].end - duration) > 0.001:
        raise ValueError("Timeline must cover the video")
    return True
