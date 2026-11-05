"""Validate reusable timed label cues before FFmpeg rendering (review-only)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str

def validate_cues(cues, duration: float):
    if duration <= 0:
        raise ValueError("duration must be positive")
    previous_end = 0.0
    for cue in cues:
        if not cue.text.strip():
            raise ValueError("empty caption")
        if not (0 <= cue.start < cue.end <= duration):
            raise ValueError("caption outside video")
        if cue.start < previous_end:
            raise ValueError("overlapping captions")
        previous_end = cue.end
    return True

def ffmpeg_enable(cue: Cue):
    return f"between(t,{cue.start:g},{cue.end:g})"
