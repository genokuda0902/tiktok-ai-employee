"""Zero-cost kinetic motion contract for portrait image-slide videos.

Keeps motion deliberately subtle so text-heavy cards remain readable. This module
only describes motion; it never publishes content and always requires human review.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MotionProfile:
    zoom_start: float
    zoom_end: float
    max_zoom_delta: float
    fps: int = 30


def kinetic_card_contract(width: int = 1080, height: int = 1920) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("kinetic cards require 1080x1920 portrait output")
    return {
        "zero_cost": True,
        "human_approval_required": True,
        "auto_post": False,
        "preserve_burned_captions": True,
        "max_zoom_delta": 0.035,
        "fps": 30,
    }


def motion_profile(index: int) -> MotionProfile:
    if index < 0:
        raise ValueError("card index must be non-negative")
    # Alternate a gentle push-in and pull-back to avoid a static slideshow feel.
    if index % 2 == 0:
        return MotionProfile(1.000, 1.035, 0.035)
    return MotionProfile(1.035, 1.000, 0.035)


def zoompan_filter(index: int, frames: int = 48) -> str:
    if frames <= 0:
        raise ValueError("frames must be positive")
    profile = motion_profile(index)
    if index % 2 == 0:
        z = "min(zoom+0.0008,1.035)"
    else:
        z = "1.035-min(on*0.0007,0.035)"
    return (
        "scale=1200:2134:flags=lanczos,"
        f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s=1080x1920:fps={profile.fps},format=yuv420p"
    )
