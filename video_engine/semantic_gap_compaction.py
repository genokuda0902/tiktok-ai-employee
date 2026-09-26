"""Zero-cost pacing helper for image-slide + Japanese narration + baked captions.

Given measured silence intervals, compute A/V cuts that keep a short natural pause while
removing only excess silence. The exact same cuts must be applied to video and audio so
baked captions and narration stay aligned. This module never posts content.
"""
from __future__ import annotations

from dataclasses import dataclass

MAX_NATURAL_PAUSE_S = 0.55
TAIL_PAUSE_S = 0.35


@dataclass(frozen=True)
class Interval:
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start


def plan_excess_silence_cuts(
    silences: list[Interval],
    total_duration_s: float,
    natural_pause_s: float = MAX_NATURAL_PAUSE_S,
) -> list[Interval]:
    """Return intervals to remove from both A/V tracks.

    Internal silences retain ``natural_pause_s`` centered on the boundary. A trailing
    silence retains ``TAIL_PAUSE_S``. Short pauses are left untouched.
    """
    if total_duration_s <= 0:
        raise ValueError("total_duration_s must be positive")
    if not 0 < natural_pause_s <= 0.8:
        raise ValueError("natural_pause_s must be in (0, 0.8]")

    cuts: list[Interval] = []
    previous_end = 0.0
    for silence in silences:
        if silence.start < previous_end or silence.end <= silence.start:
            raise ValueError("silence intervals must be ordered and non-overlapping")
        if silence.start < 0 or silence.end > total_duration_s + 1e-6:
            raise ValueError("silence interval outside media duration")
        previous_end = silence.end

        trailing = abs(silence.end - total_duration_s) <= 1e-3
        keep = TAIL_PAUSE_S if trailing else natural_pause_s
        if silence.duration <= keep:
            continue
        if trailing:
            cut_start = silence.start + keep
            cut_end = silence.end
        else:
            edge = keep / 2.0
            cut_start = silence.start + edge
            cut_end = silence.end - edge
        cuts.append(Interval(round(cut_start, 6), round(cut_end, 6)))
    return cuts


def posting_policy() -> dict:
    return {"zero_cost": True, "human_approval_required": True, "auto_post": False}
