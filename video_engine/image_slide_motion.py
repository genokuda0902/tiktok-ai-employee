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

DEFAULT_EVENTS = (
    {"start": 0.0, "processing": 0.56, "result": 1.30},
    {"start": 6.5, "processing": 0.56, "result": 1.30},
    {"start": 13.0, "processing": 0.56, "result": 1.30},
)


def _portrait(width: int, height: int) -> None:
    if width != 1080 or height != 1920:
        raise ValueError("image-slide motion currently requires 1080x1920 output")


def _validate_events(events) -> None:
    previous = -1.0
    for event in events:
        start = float(event["start"])
        processing = float(event["processing"])
        result = float(event["result"])
        if start < 0 or processing <= 0 or result <= processing or start <= previous:
            raise ValueError("events must be ordered and have valid positive phase durations")
        previous = start


def motion_filter(index: int, width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height)
    p = MOTION_PROFILES[index % len(MOTION_PROFILES)]
    sw, sh = p["scale"]
    return f"scale={sw}:{sh},crop={width}:{height}:x='{p['x']}':y='{p['y']}'"


def interaction_filter(width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height)
    x = "180+(W-360)*(0.5+0.42*sin(t*0.9))"
    y = "520+(H-900)*(0.5+0.38*cos(t*0.7))"
    pulse = "lt(mod(t,2.5),0.16)"
    return (
        f"drawbox=x='{x}':y='{y}':w=30:h=30:color=white@0.95:t=fill,"
        f"drawbox=x='{x}-12':y='{y}-12':w=54:h=54:color=white@0.30:t=3:enable='{pulse}'"
    )


def event_manifest_filter(events=DEFAULT_EVENTS, width: int = 1080, height: int = 1920) -> str:
    """Render processing/result reactions only at manifest-defined times.

    The same event data can later be generated from narration/caption timing,
    so ten genres can share one synchronization path instead of hard-coded
    periodic effects.
    """
    _portrait(width, height)
    _validate_events(events)
    layers = []
    for event in events:
        start = float(event["start"])
        processing_end = start + float(event["processing"])
        result_end = start + float(event["result"])
        processing = f"between(t,{start:.3f},{processing_end:.3f})"
        result = f"between(t,{processing_end:.3f},{result_end:.3f})"
        progress = f"min(720,720*(t-{start:.3f})/{float(event['processing']):.3f})"
        layers.extend((
            f"drawbox=x=140:y=1380:w=800:h=150:color=black@0.38:t=fill:enable='{processing}'",
            f"drawbox=x=180:y=1438:w='{progress}':h=18:color=white@0.88:t=fill:enable='{processing}'",
            f"drawbox=x=140:y=1380:w=800:h=150:color=white@0.16:t=fill:enable='{result}'",
            f"drawbox=x=820:y=1420:w=54:h=54:color=white@0.92:t=fill:enable='{result}'",
        ))
    return ",".join(layers)


def semantic_reaction_filter(width: int = 1080, height: int = 1920) -> str:
    """Backward-compatible periodic reaction used by earlier experiments."""
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


def interactive_motion_filter(index: int, width: int = 1080, height: int = 1920, events=DEFAULT_EVENTS) -> str:
    """Combine camera motion, cursor feedback and manifest-timed reactions."""
    return (
        f"{motion_filter(index, width, height)},"
        f"{interaction_filter(width, height)},"
        f"{event_manifest_filter(events, width, height)}"
    )
