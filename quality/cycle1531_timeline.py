"""Fail-closed, genre-agnostic review timeline contract (cycle1531)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Segment:
    start: float
    end: float
    caption: str

def validate_timeline(segments, duration, *, narration_verified=False,
                      rights_approved=False, human_approved=False):
    errors = []
    if duration <= 0 or not segments:
        errors.append("missing timeline")
    cursor = 0.0
    for segment in segments:
        if segment.start < cursor - 1e-6 or segment.end <= segment.start:
            errors.append("overlap or invalid segment")
        if segment.end > duration + 1e-6:
            errors.append("segment exceeds duration")
        if not segment.caption.strip():
            errors.append("empty caption")
        cursor = segment.end
    if not narration_verified:
        errors.append("Japanese narration unverified")
    if not rights_approved:
        errors.append("asset rights unapproved")
    if not human_approved:
        errors.append("human approval missing")
    return {"posting_allowed": not errors, "errors": errors}
