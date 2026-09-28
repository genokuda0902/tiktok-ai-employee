"""Genre-independent helpers for image-slide TikTok videos.

Zero-cost path. Human approval remains mandatory. The preferred route is now
image-complete cards: hook/caption/comparison/CTA copy is baked into each
1080x1920 source image before video assembly, leaving video-time filters for
subtle motion only.
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


def baked_card_manifest(cards, width: int = 1080, height: int = 1920):
    """Validate image-complete slide cards for the 10-genre common route.

    Every card carries its own headline and readable caption. BEFORE/AFTER and
    CTA are card roles, not video-time overlays. This keeps text deterministic
    and reviewable before encoding the MP4.
    """
    _portrait(width, height)
    if not cards:
        raise ValueError("at least one baked card is required")
    allowed = {"hook", "context", "step", "comparison", "result", "cta"}
    result = []
    for index, card in enumerate(cards):
        role = str(card.get("role", "")).strip()
        headline = str(card.get("headline", "")).strip()
        caption = str(card.get("caption", "")).strip()
        image = str(card.get("image", "")).strip()
        duration = float(card.get("duration", 0))
        if role not in allowed or not headline or not caption or not image or duration <= 0:
            raise ValueError(f"invalid baked card at index {index}")
        result.append({"role": role, "headline": headline, "caption": caption,
                       "image": image, "duration": duration, "text_baked": True})
    return tuple(result)


def _validate_events(events) -> None:
    previous = -1.0
    for event in events:
        start = float(event["start"]); processing = float(event["processing"]); result = float(event["result"])
        if start < 0 or processing <= 0 or result <= processing or start <= previous:
            raise ValueError("events must be ordered and have valid positive phase durations")
        previous = start


def motion_filter(index: int, width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height); p = MOTION_PROFILES[index % len(MOTION_PROFILES)]; sw, sh = p["scale"]
    return f"scale={sw}:{sh},crop={width}:{height}:x='{p['x']}':y='{p['y']}'"


def interaction_filter(width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height)
    x = "180+(W-360)*(0.5+0.42*sin(t*0.9))"; y = "520+(H-900)*(0.5+0.38*cos(t*0.7))"; pulse = "lt(mod(t,2.5),0.16)"
    return f"drawbox=x='{x}':y='{y}':w=30:h=30:color=white@0.95:t=fill,drawbox=x='{x}-12':y='{y}-12':w=54:h=54:color=white@0.30:t=3:enable='{pulse}'"


def event_manifest_filter(events=DEFAULT_EVENTS, width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height); _validate_events(events); layers = []
    for event in events:
        start=float(event['start']); pe=start+float(event['processing']); re=start+float(event['result'])
        processing=f"between(t,{start:.3f},{pe:.3f})"; result=f"between(t,{pe:.3f},{re:.3f})"; progress=f"min(720,720*(t-{start:.3f})/{float(event['processing']):.3f})"
        layers.extend((f"drawbox=x=140:y=1380:w=800:h=150:color=black@0.38:t=fill:enable='{processing}'",f"drawbox=x=180:y=1438:w='{progress}':h=18:color=white@0.88:t=fill:enable='{processing}'",f"drawbox=x=140:y=1380:w=800:h=150:color=white@0.16:t=fill:enable='{result}'",f"drawbox=x=820:y=1420:w=54:h=54:color=white@0.92:t=fill:enable='{result}'"))
    return ",".join(layers)


def _safe(text: str) -> str:
    return text.replace("'", "’").replace(":", "\\:")


def hook_hierarchy_filter(hook: str, benefit: str, fontfile: str, width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height)
    if not hook.strip() or not benefit.strip() or not fontfile.strip(): raise ValueError("hook, benefit and fontfile are required")
    h,b=_safe(hook),_safe(benefit)
    return "drawbox=x=60:y=105:w=960:h=145:color=black@0.72:t=fill:enable='between(t,0,2.8)',"+f"drawtext=fontfile='{fontfile}':text='{h}':fontcolor=white:fontsize=58:x=(w-text_w)/2:y=142:enable='between(t,0,2.8)',"+"drawbox=x=105:y=105:w=870:h=145:color=black@0.72:t=fill:enable='between(t,2.8,5.8)',"+f"drawtext=fontfile='{fontfile}':text='{b}':fontcolor=white:fontsize=62:x=(w-text_w)/2:y=140:enable='between(t,2.8,5.8)'"


def comparison_filter(before: str, after: str, fontfile: str, start: float = 8.0, end: float = 12.0, width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height)
    if not before.strip() or not after.strip() or not fontfile.strip() or start < 0 or end <= start: raise ValueError("before, after, fontfile and a valid time range are required")
    before,after=_safe(before),_safe(after); enabled=f"between(t,{start:.3f},{end:.3f})"
    return f"drawbox=x=55:y=360:w=455:h=180:color=black@0.72:t=fill:enable='{enabled}',drawtext=fontfile='{fontfile}':text='BEFORE':fontcolor=white:fontsize=34:x=90:y=390:enable='{enabled}',drawtext=fontfile='{fontfile}':text='{before}':fontcolor=white:fontsize=48:x=90:y=450:enable='{enabled}',drawbox=x=570:y=360:w=455:h=180:color=white@0.88:t=fill:enable='{enabled}',drawtext=fontfile='{fontfile}':text='AFTER':fontcolor=black:fontsize=34:x=605:y=390:enable='{enabled}',drawtext=fontfile='{fontfile}':text='{after}':fontcolor=black:fontsize=48:x=605:y=450:enable='{enabled}'"


def end_card_filter(cta: str, fontfile: str, start: float = 16.2, end: float = 19.6, width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height)
    if not cta.strip() or not fontfile.strip() or start < 0 or end <= start:
        raise ValueError("cta, fontfile and a valid time range are required")
    cta=_safe(cta); enabled=f"between(t,{start:.3f},{end:.3f})"; pulse=f"1+0.035*sin((t-{start:.3f})*8)"
    return f"drawbox=x=90:y=1240:w=900:h=220:color=black@0.78:t=fill:enable='{enabled}',drawbox=x=125:y=1280:w=830:h=140:color=white@0.12:t=fill:enable='{enabled}',drawtext=fontfile='{fontfile}':text='{cta}':fontcolor=white:fontsize=54:x=(w-text_w)/2:y=1322:enable='{enabled}',drawbox=x='440-55*({pulse}-1)':y='1450-12*({pulse}-1)':w='200+110*({pulse}-1)':h='8+24*({pulse}-1)':color=white@0.85:t=fill:enable='{enabled}'"


def semantic_reaction_filter(width: int = 1080, height: int = 1920) -> str:
    _portrait(width, height); phase="mod(t,2.5)"; processing=f"between({phase},0.16,0.72)"; result=f"between({phase},0.72,1.30)"
    return "drawbox=x=140:y=1380:w=800:h=150:color=black@0.38:t=fill:"+f"enable='{processing}',drawbox=x=180:y=1438:w='min(720,720*(mod(t,2.5)-0.16)/0.56)':h=18:color=white@0.88:t=fill:enable='{processing}',drawbox=x=140:y=1380:w=800:h=150:color=white@0.16:t=fill:enable='{result}',drawbox=x=820:y=1420:w=54:h=54:color=white@0.92:t=fill:enable='{result}'"


def interactive_motion_filter(index: int, width: int = 1080, height: int = 1920, events=DEFAULT_EVENTS) -> str:
    return f"{motion_filter(index,width,height)},{interaction_filter(width,height)},{event_manifest_filter(events,width,height)}"
