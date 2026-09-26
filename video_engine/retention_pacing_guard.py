"""Zero-cost retention pacing policy for image-first TikTok masters.

Applies one bounded whole-timeline speed factor to video and audio together so
burned captions remain synchronized. Posting stays manual and human-approved.
"""

def pacing_filter(speed: float = 1.04, width: int = 1080, height: int = 1920) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("portrait delivery must be 1080x1920")
    if not 1.0 <= speed <= 1.06:
        raise ValueError("speed must stay within 1.00..1.06")
    return {
        "video": f"setpts=PTS/{speed:.3f}",
        "audio": f"atempo={speed:.3f}",
        "speed": speed,
    }

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "whole_timeline_sync": True,
        "preserve_burned_captions": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "max_speed": 1.06,
    }
