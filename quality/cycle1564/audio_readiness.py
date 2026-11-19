"""Fail-closed narration readiness gate; never infer speech from AAC presence."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    has_audio_stream: bool
    verified_japanese_speech: bool
    transcript_verified: bool
    captions_aligned: bool
    rights_cleared: bool
    employee_approved: bool

def review(e: Evidence) -> dict:
    checks = {
        "audio_stream": e.has_audio_stream,
        "japanese_speech": e.verified_japanese_speech,
        "transcript": e.transcript_verified,
        "speech_caption_alignment": e.captions_aligned,
        "rights": e.rights_cleared,
        "employee_approval": e.employee_approved,
    }
    return {"publication_approved": all(checks.values()), "missing": [k for k,v in checks.items() if not v]}
