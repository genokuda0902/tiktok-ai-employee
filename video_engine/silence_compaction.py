"""Zero-cost narration silence compaction for image-slide TikTok masters.

Long narration gaps reduce perceived pace. This helper converts measured silence
intervals into A/V cuts while preserving a short readable pause. The exact same
ranges are removed from video and audio, so approved baked captions are never
retimed independently from their image. Human approval and manual posting remain
mandatory.
"""

from typing import Iterable, List, Tuple


def removal_ranges(
    silences: Iterable[Tuple[float, float]],
    *,
    max_pause: float = 0.45,
    duration: float,
) -> List[Tuple[float, float]]:
    if duration <= 0:
        raise ValueError("duration must be positive")
    if not 0.20 <= max_pause <= 0.75:
        raise ValueError("max_pause must stay within the reviewed 0.20-0.75s range")
    cuts: List[Tuple[float, float]] = []
    last_end = 0.0
    for start, end in silences:
        start, end = float(start), float(end)
        if start < 0 or end <= start or end > duration or start < last_end:
            raise ValueError("silence intervals must be ordered, valid and in bounds")
        if end - start > max_pause:
            cuts.append((start + max_pause, end))
        last_end = end
    return cuts


def keep_ranges(cuts: Iterable[Tuple[float, float]], *, duration: float) -> List[Tuple[float, float]]:
    cursor = 0.0
    keep: List[Tuple[float, float]] = []
    for start, end in cuts:
        if start < cursor or end <= start or end > duration:
            raise ValueError("cut intervals must be ordered, valid and in bounds")
        if start > cursor:
            keep.append((cursor, start))
        cursor = end
    if cursor < duration:
        keep.append((cursor, duration))
    return keep


def sync_contract(max_pause: float = 0.45) -> dict:
    return {
        "max_pause": float(max_pause),
        "cut_video_and_audio_together": True,
        "caption_copy_unchanged": True,
        "zero_cost": True,
        "human_approval_required": True,
        "auto_post": False,
    }
