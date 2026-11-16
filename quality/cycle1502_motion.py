"""Review-only gentle motion filter for image-first vertical videos.

Never claims narration, asset rights, subtitle sync, or publication approval.
"""
from __future__ import annotations

def zoompan_filter(width: int = 720, height: int = 1280, fps: int = 24) -> str:
    if width <= 0 or height <= 0 or fps <= 0:
        raise ValueError("dimensions and fps must be positive")
    # Scale first to leave a safe margin for the moving crop.
    source_width = round(width * 13 / 12)
    source_height = round(height * 13 / 12)
    return (
        f"scale={source_width}:{source_height},"
        "zoompan=z='min(zoom+0.00075,1.06)':"
        "x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':"
        f"d=1:s={width}x{height}:fps={fps},format=yuv420p"
    )

def publication_preflight(*, japanese_speech_verified: bool,
                          subtitle_sync_verified: bool,
                          assets_approved: bool,
                          employee_approved: bool) -> bool:
    return all((japanese_speech_verified, subtitle_sync_verified,
                assets_approved, employee_approved))
