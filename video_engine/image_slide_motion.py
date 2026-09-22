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
    """Render processing/result reactions only at manifest-defined times."""
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


def hook_hierarchy_filter(hook: str, benefit: str, fontfile: str, width: int = 1080, height: int = 1920) -> str:
    """Show a short hook then benefit card in the top safe area."""
    _portrait(width, height)
    if not hook.strip() or not benefit.strip() or not fontfile.strip():
        raise ValueError("hook, benefit and fontfile are required")
    safe_hook = hook.replace("'", "’").replace(":", "\\:")
    safe_benefit = benefit.replace("'", "’").replace(":", "\\:")
    return (
        "drawbox=x=60:y=105:w=960:h=145:color=black@0.72:t=fill:enable='between(t,0,2.8)',"
        f"drawtext=fontfile='{fontfile}':text='{safe_hook}':fontcolor=white:fontsize=58:x=(w-text_w)/2:y=142:enable='between(t,0,2.8)',"
        "drawbox=x=105:y=105:w=870:h=145:color=black@0.72:t=fill:enable='between(t,2.8,5.8)',"
        f"drawtext=fontfile='{fontfile}':text='{safe_benefit}':fontcolor=white:fontsize=62:x=(w-text_w)/2:y=140:enable='between(t,2.8,5.8)'"
    )


def comparison_filter(before: str, after: str, fontfile: str, start: float = 8.0, end: float = 12.0, width: int = 1080, height: int = 1920) -> str:
    """Add a genre-independent BEFORE/AFTER comparison beat.

    Labels are caller supplied so the same timing/layout can be reused across
    all genre profiles without implying a result the source material cannot support.
    """
    _portrait(width, height)
    if not before.strip() or not after.strip() or not fontfile.strip() or start < 0 or end <= start:
        raise ValueError("before, after, fontfile and a valid time range are required")
    safe_before = before.replace("'", "’").replace(":", "\\:")
    safe_after = after.replace("'", "’").replace(":", "\\:")
    enabled = f"between(t,{start:.3f},{end:.3f})"
    return (
        f"drawbox=x=55:y=360:w=455:h=180:color=black@0.72:t=fill:enable='{enabled}',"
        f"drawtext=fontfile='{fontfile}':text='BEFORE':fontcolor=white:fontsize=34:x=90:y=390:enable='{enabled}',"
        f"drawtext=fontfile='{fontfile}':text='{safe_before}':fontcolor=white:fontsize=48:x=90:y=450:enable='{enabled}',"
        f"drawbox=x=570:y=360:w=455:h=180:color=white@0.88:t=fill:enable='{enabled}',"
        f"drawtext=fontfile='{fontfile}':text='AFTER':fontcolor=black:fontsize=34:x=605:y=390:enable='{enabled}',"
        f"drawtext=fontfile='{fontfile}':text='{safe_after}':fontcolor=black:fontsize=48:x=605:y=450:enable='{enabled}'"
    )


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
