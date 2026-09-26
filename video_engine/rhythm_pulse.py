"""Zero-cost rhythmic visual pulse for image-slide TikTok masters.

Applies only a subtle, short luminance emphasis at scene-beat boundaries.
It does not alter caption copy, narration, posting policy, or rights approval.
"""

def pulse_windows(duration: float, interval: float = 1.10, pulse: float = 0.10):
    if duration <= 0 or not (0.8 <= interval <= 2.0) or not (0.05 <= pulse <= 0.15):
        raise ValueError("unsafe rhythm pulse settings")
    out=[]
    t=0.0
    while t < duration:
        out.append((round(t,3), round(min(t+pulse,duration),3)))
        t += interval
    return out

def ffmpeg_filter(duration: float) -> str:
    wins=pulse_windows(duration)
    expr="+".join(f"between(t,{a:.2f},{b:.2f})" for a,b in wins)
    return f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.10:t=fill:enable='{expr}'"

def release_contract():
    return {
        "zero_cost": True,
        "delivery": (1080,1920,30),
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
