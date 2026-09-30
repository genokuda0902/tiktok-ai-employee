"""Reusable TikTok caption safe-zone contract.

Reimplementation quality guard. It does not imply content approval.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class CaptionBox:
    top: int
    height: int

def validate_caption_safezone(frame_height: int, box: CaptionBox, *, lower_ui_ratio: float = 0.20, min_clearance_px: int = 24) -> int:
    if frame_height <= 0 or box.top < 0 or box.height <= 0:
        raise ValueError("invalid geometry")
    boundary = int(frame_height * (1.0 - lower_ui_ratio))
    bottom = box.top + box.height
    clearance = boundary - bottom
    if clearance < min_clearance_px:
        raise ValueError(f"caption safe-zone violation: clearance={clearance}px required={min_clearance_px}px")
    return clearance
