"""Review-only narration evidence gate. A soundtrack is not proof of Japanese speech."""
from dataclasses import dataclass

@dataclass(frozen=True)
class NarrationEvidence:
    audio_stream_present: bool
    japanese_speech_verified: bool
    caption_alignment_verified: bool
    asset_rights_approved: bool
    staff_approved: bool

def publication_eligible(evidence: NarrationEvidence) -> bool:
    return all((
        evidence.audio_stream_present,
        evidence.japanese_speech_verified,
        evidence.caption_alignment_verified,
        evidence.asset_rights_approved,
        evidence.staff_approved,
    ))
