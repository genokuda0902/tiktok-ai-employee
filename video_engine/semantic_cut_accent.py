"""Zero-cost semantic cut accent for image-first TikTok renders.

Reimplementation helper: adds a very short luminance lift at semantic scene boundaries
without changing audio/caption timing. Human quality/rights approval remains mandatory;
this module never posts content.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CutAccentPolicy:
    width: int = 1080
    height: int = 1920
    accent_seconds: float = 0.10
    brightness: float = 0.035
    max_brightness: float = 0.05

    def validate(self) -> None:
        if (self.width, self.height) != (1080, 1920):
            raise ValueError("semantic cut accent is restricted to 1080x1920")
        if not 0.04 <= self.accent_seconds <= 0.14:
            raise ValueError("accent must stay brief")
        if not 0.0 < self.brightness <= self.max_brightness:
            raise ValueError("brightness exceeds safe subtle-motion limit")


def ffmpeg_enable_expression(boundaries: list[float], policy: CutAccentPolicy | None = None) -> str:
    """Return an FFmpeg enable expression for short accents at semantic boundaries."""
    policy = policy or CutAccentPolicy()
    policy.validate()
    clean = sorted({round(float(t), 3) for t in boundaries if float(t) > 0})
    if not clean:
        raise ValueError("at least one positive semantic boundary is required")
    return "+".join(f"between(t,{t:.3f},{t + policy.accent_seconds:.3f})" for t in clean)


def eq_filter(boundaries: list[float], policy: CutAccentPolicy | None = None) -> str:
    policy = policy or CutAccentPolicy()
    expr = ffmpeg_enable_expression(boundaries, policy)
    return f"eq=brightness={policy.brightness:.3f}:enable='{expr}'"


HUMAN_APPROVAL_REQUIRED = True
AUTO_POST_ALLOWED = False
