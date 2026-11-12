"""Shared 10-genre typing animation timing. Review-only; no publication approval."""
from dataclasses import dataclass

@dataclass(frozen=True)
class TypingCue:
    text: str
    start: float
    duration: float

def visible_text(cue: TypingCue, timestamp: float) -> str:
    if cue.duration <= 0 or cue.start < 0:
        raise ValueError("invalid timing")
    if timestamp <= cue.start:
        return ""
    progress = min(1.0, max(0.0, (timestamp - cue.start) / cue.duration))
    return cue.text[:int(len(cue.text) * progress)]

def publishable(*, japanese_voice_verified: bool, speech_sync_verified: bool,
                rights_approved: bool, employee_approved: bool) -> bool:
    return all((japanese_voice_verified, speech_sync_verified,
                rights_approved, employee_approved))
