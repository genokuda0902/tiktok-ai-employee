"""Genre-independent motion helpers for image-slide TikTok videos.

Zero-cost FFmpeg path. This module does not publish videos and does not claim
visual quality; human approval remains mandatory.
"""

MOTION_PROFILES = (
    {"scale": (1120, 1992), "x": "20+20*sin(t*0.7)", "y": "36+20*sin(t*0.5)"},
    {"scale": (1140, 2027), "x": "30+25*sin(t*0.6)", "y": "53+25*cos(t*0.45)"},
    {"scale": (1120, 1992), "x": "20+18*cos(t*0.65)", "y": "36+22*sin(t*0.55)"},
    {"scale": (1150, 2044), "x": "35+30*sin(t*0.55)", "y": "62+30*cos(t*0.4)"},
)


def _portrait(width: int, height: int) -> None:
    if width != 1080 or height != 1920:
        raise ValueError("image-slide motion currently requires 1080x1920 output")


def motion_filter(index: int, width: int = 1080, height: int = 1920) -> str:
    """Return a subtle pan/zoom crop filter for a portrait scene."""
    _portrait(width, height)
    p = MOTION_PROFILES[index % len(MOTION_PROFILES)]
    sw, sh = p["scale"]
    return f"scale={sw}:{sh},crop={width}:{height}:x='{p['x']}':y='{p['y']}'"


def interaction_filter(width: int = 1080, height: int = 1920) -> str:
    """Add reusable cursor/click feedback without external paid assets."""
    _portrait(width, height)
    x = "180+(W-360)*(0.5+0.42*sin(t*0.9))"
    y = "520+(H-900)*(0.5+0.38*cos(t*0.7))"
    pulse = "lt(mod(t,2.5),0.16)"
    return (
        f"drawbox=x='{x}':y='{y}':w=30:h=30:color=white@0.95:t=fill,"
        f"drawbox=x='{x}-12':y='{y}-12':w=54:h=54:color=white@0.30:t=3:enable='{pulse}'"
    )


def semantic_reaction_filter(width: int = 1080, height: int = 1920) -> str:
    """Show cause -> processing -> result feedback after each generic click.

    This keeps the zero-cost route reusable across genres: no product-specific
    labels or assets are required. The three visual states make interaction
    causal rather than decorative, while narration/caption timing can later
    drive the same events from a manifest.
    """
    _portrait(width, height)
    phase = "mod(t,2.5)"
    processing = f"between({phase},0.16,0.72)"
    result = f"between({phase},0.72,1.30)"
    return (
        "drawbox=x=140:y=1380:w=800:h=150:color=black@0.38:t=fill:"
        f"enable='{processing}',"
        "drawbox=x=180:y=1438:w='min(720,720*(mod(t,2.5)-0.16)/0.56)':h=18:"
        f"color=white@0.88:t=fill:enable='{processing}',"
        "drawbox=x=140:y=1380:w=800:h=150:color=white@0.16:t=fill:"
        f"enable='{result}',"
        "drawbox=x=820:y=1420:w=54:h=54:color=white@0.92:t=fill:"
        f"enable='{result}'"
    )


def interactive_motion_filter(index: int, width: int = 1080, height: int = 1920) -> str:
    """Combine camera motion, cursor feedback and semantic result reaction."""
    return (
        f"{motion_filter(index, width, height)},"
        f"{interaction_filter(width, height)},"
        f"{semantic_reaction_filter(width, height)}"
    )
