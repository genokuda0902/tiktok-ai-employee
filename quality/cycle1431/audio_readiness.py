"""Fail-closed audio classification: AAC track alone is not narration."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AudioEvidence:
    audio_track: bool
    japanese_speech_verified: bool
    captions_synchronized: bool
    rights_approved: bool


def narration_ready(evidence: AudioEvidence) -> bool:
    return all((evidence.audio_track, evidence.japanese_speech_verified,
                evidence.captions_synchronized, evidence.rights_approved))
