"""Zero-cost semantic beat punch for image-slide TikTok renders.

Adds short, subtle scale emphasis at semantic scene boundaries so static-image
slides feel intentionally edited rather than continuously drifting. Designed as
a genre-independent finishing primitive. It does not post or approve content.
"""
from dataclasses import dataclass

MAX_SCALE = 1.025
MAX_PUNCH_S = 0.22

@dataclass(frozen=True)
class BeatPunch:
    start_s: float
    duration_s: float = 0.18
    scale: float = 1.018


def validate_punches(punches: list[BeatPunch], total_duration_s: float) -> None:
    if total_duration_s <= 0:
        raise ValueError("total duration must be positive")
    last = -1.0
    for p in punches:
        if p.start_s < 0 or p.start_s >= total_duration_s:
            raise ValueError("punch start must be inside video")
        if p.start_s <= last:
            raise ValueError("punches must be strictly ordered")
        if not (0 < p.duration_s <= MAX_PUNCH_S):
            raise ValueError("punch duration exceeds safe limit")
        if not (1.0 < p.scale <= MAX_SCALE):
            raise ValueError("punch scale exceeds safe limit")
        last = p.start_s


def ffmpeg_scale_expr(punches: list[BeatPunch], total_duration_s: float) -> str:
    """Return a bounded FFmpeg scale expression for semantic beat emphasis."""
    validate_punches(punches, total_duration_s)
    expr = "1"
    for p in punches:
        end = p.start_s + p.duration_s
        expr += f"+{p.scale-1:.4f}*between(t,{p.start_s:.3f},{end:.3f})"
    return expr


def posting_policy() -> dict:
    return {"zero_cost": True, "human_approval_required": True, "auto_post": False}
