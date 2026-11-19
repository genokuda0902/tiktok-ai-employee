"""Reusable fail-closed caption and narration evidence checks for review renders."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RenderEvidence:
    has_burned_captions: bool
    japanese_speech_verified: bool
    transcript_sync_verified: bool
    rights_approved: bool
    employee_approved: bool

def publication_ready(e: RenderEvidence) -> bool:
    return all((e.has_burned_captions, e.japanese_speech_verified,
                e.transcript_sync_verified, e.rights_approved,
                e.employee_approved))
