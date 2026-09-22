"""Genre-independent motion filter helpers for image-slide TikTok videos.

Zero-cost FFmpeg path. This module does not publish videos and does not claim
visual quality; human approval remains mandatory.
"""

MOTION_PROFILES = (
    {"scale": (1120, 1992), "x": "20+20*sin(t*0.7)", "y": "36+20*sin(t*0.5)"},
    {"scale": (1140, 2027), "x": "30+25*sin(t*0.6)", "y": "53+25*cos(t*0.45)"},
    {"scale": (1120, 1992), "x": "20+18*cos(t*0.65)", "y": "36+22*sin(t*0.55)"},
    {"scale": (1150, 2044), "x": "35+30*sin(t*0.55)", "y": "62+30*cos(t*0.4)"},
)


def motion_filter(index: int, width: int = 1080, height: int = 1920) -> str:
    """Return a subtle pan/zoom crop filter for a portrait scene."""
    if width != 1080 or height != 1920:
        raise ValueError("image-slide motion currently requires 1080x1920 output")
    p = MOTION_PROFILES[index % len(MOTION_PROFILES)]
    sw, sh = p["scale"]
    return f"scale={sw}:{sh},crop={width}:{height}:x='{p['x']}':y='{p['y']}'"
