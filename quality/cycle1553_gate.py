"""Fail-closed publication gate, independent of video codec presence."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Evidence:
    audio_stream: bool
    japanese_narration_verified: bool
    caption_alignment_verified: bool
    assets_approved: bool
    human_approved: bool

def publication_ready(e: Evidence) -> bool:
    return all((e.audio_stream, e.japanese_narration_verified,
                e.caption_alignment_verified, e.assets_approved,
                e.human_approved))
