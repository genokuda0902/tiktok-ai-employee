"""Fail-closed evidence contract for Japanese narration; shared across genres."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AudioProof:
    has_audio_stream: bool
    narration_transcript: str
    japanese_speech_verified: bool
    caption_alignment_verified: bool
    assets_approved: bool
    employee_approved: bool

def publication_allowed(proof: AudioProof) -> bool:
    """An AAC stream or a tone is never sufficient evidence of narration."""
    return all((
        proof.has_audio_stream,
        bool(proof.narration_transcript.strip()),
        proof.japanese_speech_verified,
        proof.caption_alignment_verified,
        proof.assets_approved,
        proof.employee_approved,
    ))
