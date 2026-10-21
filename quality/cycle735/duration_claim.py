"""Shared duration-claim policy for all ten TikTok content genres."""
from math import ceil


def duration_claim(video_seconds: float) -> str:
    """Return an honest, rounded-up Japanese video duration label."""
    if not 0 < video_seconds < 3600:
        raise ValueError("video_seconds must be positive and less than an hour")
    return f"{ceil(video_seconds - 0.000001)}秒でわかる"


def scene_boundaries(frame_counts: list[int], fps: int = 30) -> list[float]:
    """Return cumulative scene transition times for a fixed-frame-rate edit."""
    if fps <= 0 or not frame_counts or any(n <= 0 for n in frame_counts):
        raise ValueError("invalid scene durations")
    total = 0
    times = []
    for frames in frame_counts[:-1]:
        total += frames
        times.append(total / fps)
    return times
