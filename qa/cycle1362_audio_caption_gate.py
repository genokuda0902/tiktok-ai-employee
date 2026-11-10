"""Fail-closed QA for silent review-only renders (cycle1362)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class AudioCaptionQA:
    audio_stream_present: bool
    japanese_narration_verified: bool
    captions_visible: bool
    captions_synced_to_speech: bool
    assets_approved: bool
    employee_approved: bool

def publication_allowed(q: AudioCaptionQA) -> bool:
    return all((q.audio_stream_present, q.japanese_narration_verified,
                q.captions_visible, q.captions_synced_to_speech,
                q.assets_approved, q.employee_approved))
