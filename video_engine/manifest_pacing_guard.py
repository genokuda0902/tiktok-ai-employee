"""Genre-independent pacing guard for manifest-driven TikTok videos.

Zero-cost and fail-closed: validates story duration/cut count before rendering.
"""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class PacingResult:
    total_seconds: float
    cut_count: int
    avg_cut_seconds: float

def validate_pacing(durations: Iterable[float], *, min_cuts: int = 8, max_cuts: int = 12,
                    min_total: float = 24.0, max_total: float = 45.0,
                    min_cut: float = 1.2, max_cut: float = 5.5) -> PacingResult:
    ds = [float(x) for x in durations]
    if not (min_cuts <= len(ds) <= max_cuts):
        raise ValueError("cut count outside 8-12 contract")
    if any(d < min_cut or d > max_cut for d in ds):
        raise ValueError("individual cut duration outside pacing bounds")
    total = round(sum(ds), 3)
    if not (min_total <= total <= max_total):
        raise ValueError("total duration outside 24-45s contract")
    return PacingResult(total, len(ds), round(total / len(ds), 3))

def release_contract():
    return {
        "zero_cost": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "genre_independent": True,
    }
