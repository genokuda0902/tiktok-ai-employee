"""Zero-cost speech-aware caption visibility gate.

Keeps semantic captions visible only while narration is active. Silence intervals are
provided by local audio analysis (for example FFmpeg silencedetect); no paid API or
cloud transcription is required. This module does not publish or upload media.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    start_s: float
    end_s: float


def validate_silences(silences: list[Interval], duration_s: float) -> None:
    if duration_s <= 0:
        raise ValueError("duration must be positive")
    previous_end = 0.0
    for item in silences:
        if item.start_s < previous_end or item.end_s <= item.start_s:
            raise ValueError("silence intervals must be ordered and non-overlapping")
        if item.start_s < 0 or item.end_s > duration_s + 0.04:
            raise ValueError("silence interval outside media duration")
        previous_end = item.end_s


def speech_intervals(silences: list[Interval], duration_s: float, min_speech_s: float = 0.08) -> list[Interval]:
    validate_silences(silences, duration_s)
    out: list[Interval] = []
    cursor = 0.0
    for silence in silences:
        if silence.start_s - cursor >= min_speech_s:
            out.append(Interval(cursor, silence.start_s))
        cursor = silence.end_s
    if duration_s - cursor >= min_speech_s:
        out.append(Interval(cursor, duration_s))
    return out


def render_policy() -> dict:
    return {
        "zero_cost": True,
        "local_audio_analysis_only": True,
        "caption_hidden_during_silence": True,
        "japanese_caption_layer": True,
        "human_quality_review_required": True,
        "human_rights_review_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
