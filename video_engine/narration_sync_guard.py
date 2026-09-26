"""Fail-closed narration/caption timing guard for image-first TikTok stories.

Reimplementation helper only. It does not synthesize speech, upload media, or post.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class CutTiming:
    narration: str
    caption: str
    planned_duration: float
    audio_duration: float

def _norm(s: str) -> str:
    return "".join(s.split())

def validate_narration_sync(cuts: Sequence[CutTiming], *, max_drift: float = 0.25,
                            min_unique_ratio: float = 0.90) -> dict:
    if not 8 <= len(cuts) <= 12:
        raise ValueError("image-first stories require 8-12 cuts")
    if not 0 < max_drift <= 0.50:
        raise ValueError("max_drift must be >0 and <=0.50 seconds")
    narrations = []
    total_planned = 0.0
    total_audio = 0.0
    for i, cut in enumerate(cuts):
        n, c = _norm(cut.narration), _norm(cut.caption)
        if not n or not c:
            raise ValueError(f"cut {i} missing narration/caption")
        if c not in n:
            raise ValueError(f"cut {i} caption drifts from narration")
        if cut.planned_duration <= 0 or cut.audio_duration <= 0:
            raise ValueError(f"cut {i} invalid duration")
        if abs(cut.planned_duration-cut.audio_duration) > max_drift:
            raise ValueError(f"cut {i} audio/timeline drift exceeds tolerance")
        narrations.append(n)
        total_planned += cut.planned_duration
        total_audio += cut.audio_duration
    unique_ratio = len(set(narrations))/len(narrations)
    if unique_ratio < min_unique_ratio:
        raise ValueError("narration reuse exceeds uniqueness threshold")
    if abs(total_planned-total_audio) > max_drift:
        raise ValueError("story audio/timeline drift exceeds tolerance")
    return {
        "cuts": len(cuts),
        "unique_ratio": round(unique_ratio, 3),
        "planned_duration": round(total_planned, 3),
        "audio_duration": round(total_audio, 3),
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "zero_cost": True,
    }
