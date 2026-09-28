"""Zero-cost audio edge guard for TikTok renders.

Adds very short fades only at stream boundaries to prevent end clicks/pops.
Does not alter video and is genre-independent.
"""
from __future__ import annotations


def build_edge_filter(duration_s: float, fade_in_s: float = 0.02, fade_out_s: float = 0.08) -> str:
    if duration_s <= 0:
        raise ValueError("duration_s must be positive")
    if not (0 <= fade_in_s <= 0.10):
        raise ValueError("fade_in_s must be 0..0.10")
    if not (0 < fade_out_s <= 0.15):
        raise ValueError("fade_out_s must be >0..0.15")
    if fade_out_s >= duration_s:
        raise ValueError("fade_out_s must be shorter than duration")
    out_start = duration_s - fade_out_s
    parts = []
    if fade_in_s:
        parts.append(f"afade=t=in:st=0:d={fade_in_s:.3f}")
    parts.append(f"afade=t=out:st={out_start:.3f}:d={fade_out_s:.3f}")
    return ",".join(parts)
