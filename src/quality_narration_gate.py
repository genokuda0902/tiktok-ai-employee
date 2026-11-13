"""Fail-closed QA for review-only video output; standard library only.

An AAC stream can contain silence, so audio presence is never narration proof.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class VideoEvidence:
    width: int
    height: int
    video_decodes: bool
    audio_stream_present: bool
    japanese_narration_verified: bool
    speech_caption_sync_verified: bool
    assets_approved: bool
    human_quality_approved: bool

def publication_gate(e: VideoEvidence) -> tuple[bool, list[str]]:
    failures = []
    if (e.width, e.height) != (1080, 1920):
        failures.append("resolution")
    if not e.video_decodes:
        failures.append("decode")
    if not e.audio_stream_present or not e.japanese_narration_verified:
        failures.append("narration")
    if not e.speech_caption_sync_verified:
        failures.append("caption_sync")
    if not e.assets_approved:
        failures.append("assets")
    if not e.human_quality_approved:
        failures.append("human_approval")
    return not failures, failures
