"""Cycle156: fail-closed visual clutter policy for image-slide videos."""
from dataclasses import dataclass

@dataclass(frozen=True)
class OverlayPolicy:
    max_transient_overlays_per_scene: int = 1
    forbid_full_width_overlay_over_existing_headline: bool = True
    preserve_caption_safe_zone: bool = True


def validate_overlay_count(count: int, policy: OverlayPolicy = OverlayPolicy()) -> None:
    if count < 0:
        raise ValueError("overlay count must be >= 0")
    if count > policy.max_transient_overlays_per_scene:
        raise ValueError("visual clutter gate failed: too many transient overlays")
