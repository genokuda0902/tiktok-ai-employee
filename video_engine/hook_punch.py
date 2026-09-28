"""Zero-cost micro punch-in for image-first TikTok hooks.

Reimplementation helper: preserves narration/captions and never posts automatically.
Human rights/quality approval remains mandatory.
"""
from __future__ import annotations


def hook_punch_filter(start: float = 0.65, duration: float = 0.25, scale: float = 1.037) -> str:
    if not (0.0 <= start <= 1.5):
        raise ValueError("hook punch must stay in opening 1.5s")
    if not (0.12 <= duration <= 0.40):
        raise ValueError("duration outside subtle punch range")
    if not (1.01 <= scale <= 1.06):
        raise ValueError("scale outside subtle punch range")
    end = start + duration
    w = round(1080 * scale / 2) * 2
    h = round(1920 * scale / 2) * 2
    return (
        f"trim=start={start}:end={end},setpts=PTS-STARTPTS,"
        f"scale={w}:{h},crop=1080:1920:x='(iw-ow)/2':y='(ih-oh)/2'"
    )


def safety_contract() -> dict[str, object]:
    return {
        "width": 1080,
        "height": 1920,
        "zero_cost": True,
        "preserve_audio": True,
        "preserve_captions": True,
        "human_approval_required": True,
        "auto_post": False,
    }
