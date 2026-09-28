"""Fail-closed TikTok safe-zone contract for deterministic overlays.

Keeps generated copy away from common top/bottom/right-side app chrome.
This module only validates layout metadata; it does not post or call paid services.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class SafeZone:
    left: int = 54
    right: int = 180
    top: int = 120
    bottom: int = 360

def validate_safe_zone(width: int, height: int, zone: SafeZone = SafeZone()) -> None:
    if (width, height) != (1080, 1920):
        raise ValueError("safe-zone contract requires 1080x1920")
    if min(zone.left, zone.right, zone.top, zone.bottom) < 0:
        raise ValueError("safe-zone margins cannot be negative")
    if zone.left + zone.right >= width or zone.top + zone.bottom >= height:
        raise ValueError("safe-zone leaves no usable content area")

def validate_box(x: int, y: int, w: int, h: int, zone: SafeZone = SafeZone()) -> None:
    validate_safe_zone(1080, 1920, zone)
    if min(x, y, w, h) < 0 or w == 0 or h == 0:
        raise ValueError("invalid overlay box")
    if x < zone.left or y < zone.top:
        raise ValueError("overlay enters left/top reserved UI area")
    if x + w > 1080 - zone.right:
        raise ValueError("overlay enters right-side TikTok UI area")
    if y + h > 1920 - zone.bottom:
        raise ValueError("overlay enters bottom caption/navigation area")

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "portrait_delivery": (1080, 1920),
        "deterministic_overlay_safe_zone": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
