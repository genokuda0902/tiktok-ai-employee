"""Zero-cost compact caption-panel transform for portrait image-slide videos.

This helper reduces an oversized burned-in caption panel without changing caption
copy or narration. It is intended as a migration aid until captions are rendered
as independent timed layers. Human rights/quality approval and manual posting
remain mandatory.
"""


def compact_caption_filter(
    width: int = 1080,
    height: int = 1920,
    source_y: int = 1480,
    source_h: int = 180,
    target_h: int = 140,
    target_y: int = 1500,
) -> str:
    if (width, height) != (1080, 1920):
        raise ValueError("portrait delivery must be 1080x1920")
    if not (100 <= source_h <= 220):
        raise ValueError("source caption crop is outside safe bounds")
    if not (100 <= target_h <= 160):
        raise ValueError("target caption panel is outside safe bounds")
    if target_h >= source_h:
        raise ValueError("caption panel must become more compact")
    if source_y < 1200 or source_y + 440 > height:
        raise ValueError("caption cleanup region is outside frame")
    if target_y < 1300 or target_y + target_h > 1750:
        raise ValueError("caption target must remain inside mobile safe region")
    return (
        f"[0:v]split=2[base][cap];"
        f"[cap]crop={width}:{source_h}:0:{source_y},"
        f"scale={width}:{target_h}:flags=lanczos[cap2];"
        f"[base]drawbox=x=0:y={source_y}:w={width}:h=440:color=0xE7EBE9:t=fill[clean];"
        f"[clean][cap2]overlay=0:{target_y}:format=auto[v]"
    )


def release_policy() -> dict:
    return {
        "zero_cost": True,
        "width": 1080,
        "height": 1920,
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "temporary_migration_transform": True,
    }
