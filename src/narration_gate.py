"""Fail-closed publication gate for Japanese narration (cycle1666).

A codec/audio stream or SFX alone is NOT evidence of spoken Japanese.
This gate accepts independently reviewed narration evidence only.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class NarrationEvidence:
    audio_stream: bool
    japanese_speech_verified: bool
    transcript: str
    caption_sync_verified: bool
    approved_assets: bool
    employee_approved: bool

def publication_allowed(e: NarrationEvidence) -> bool:
    return all((e.audio_stream, e.japanese_speech_verified,
                bool(e.transcript.strip()), e.caption_sync_verified,
                e.approved_assets, e.employee_approved))
