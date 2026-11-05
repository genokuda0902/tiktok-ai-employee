"""Fail-closed, genre-independent review gate for Japanese narration/captions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Caption:
    start: float
    end: float
    text: str

def validate_review(duration, captions, *, audio_verified=False, japanese_speech_verified=False, rights_approved=False):
    issues = []
    if duration <= 0: issues.append("invalid_duration")
    if not captions: issues.append("missing_captions")
    previous = 0.0
    for c in captions:
        if not c.text.strip(): issues.append("empty_caption")
        if c.start < previous or c.end <= c.start or c.end > duration:
            issues.append("invalid_caption_timing")
        previous = max(previous, c.end)
    if not audio_verified: issues.append("audio_not_verified")
    if not japanese_speech_verified: issues.append("japanese_speech_not_verified")
    if not rights_approved: issues.append("rights_not_approved")
    return {"approved": not issues, "issues": sorted(set(issues))}
