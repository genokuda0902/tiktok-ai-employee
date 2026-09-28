"""Zero-cost opening hook punch-in for image-first TikTok renders."""
def hook_scale(t: float, duration: float = 1.2, start: float = 1.055) -> float:
    if duration <= 0 or start < 1.0:
        raise ValueError("invalid hook profile")
    p = min(max(t / duration, 0.0), 1.0)
    return start + (1.0 - start) * p

def ffmpeg_hook_filter(duration: float = 1.2) -> str:
    if duration <= 0:
        raise ValueError("duration must be positive")
    # 5.5% opening punch-in eases back to full-frame; no paid assets/services.
    return (
        "scale=1140:2026:flags=lanczos,"
        f"crop=1080:1920:x='30*(1-min(t/{duration},1))':"
        f"y='53*(1-min(t/{duration},1))',"
        "scale=1080:1920:flags=lanczos"
    )
