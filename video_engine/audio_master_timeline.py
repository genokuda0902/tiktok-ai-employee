"""Audio-master timeline utilities for the image-first TikTok route.

Keeps the rendered visual timeline locked to narration duration so short
transitions cannot silently shorten the video and drift captions/CTA timing.
Zero-cost and genre-independent. Human rights/quality approval remains required.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TimelineResult:
    audio_duration: float
    video_duration: float
    pad_duration: float
    drift: float


def audio_master_timeline(audio_duration: float, video_duration: float, tolerance: float = 0.04) -> TimelineResult:
    if audio_duration <= 0 or video_duration <= 0:
        raise ValueError("durations must be positive")
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    drift = audio_duration - video_duration
    pad = max(0.0, drift) if drift > tolerance else 0.0
    final_video = video_duration + pad
    return TimelineResult(audio_duration, final_video, pad, audio_duration - final_video)


def ffmpeg_tail_hold_filter(pad_duration: float) -> str:
    if pad_duration < 0:
        raise ValueError("pad_duration must be non-negative")
    return f"tpad=stop_mode=clone:stop_duration={pad_duration:.3f}"
