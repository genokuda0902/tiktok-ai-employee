"""Timing guard for image-first TikTok story manifests.

Keeps 8-12 cut stories readable and avoids dead-air pacing drift.
No posting, network, paid service, or credential handling.
"""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class TimingPolicy:
    min_cut: float = 0.8
    max_cut: float = 4.0
    min_total: float = 8.0
    max_total: float = 45.0
    max_adjacent_ratio: float = 2.5

def validate_cut_durations(durations: Sequence[float], policy: TimingPolicy = TimingPolicy()) -> float:
    if not 8 <= len(durations) <= 12:
        raise ValueError("image-first stories require 8-12 cuts")
    if any(d < policy.min_cut or d > policy.max_cut for d in durations):
        raise ValueError("cut duration outside readable range")
    total = sum(durations)
    if total < policy.min_total or total > policy.max_total:
        raise ValueError("story duration outside supported range")
    for a, b in zip(durations, durations[1:]):
        ratio = max(a, b) / min(a, b)
        if ratio > policy.max_adjacent_ratio:
            raise ValueError("adjacent cuts have excessive pacing drift")
    return round(total, 3)
