"""Zero-cost cleanup for accidental production/meta labels at the top edge.

Designed for the image-slide route only. It masks a bounded top strip when the
source render contains internal stage badges clipped into TikTok's top UI area.
Human review remains mandatory; this never posts automatically.
"""


def ffmpeg_filter(width=1080, height=1920, strip_height=105, color="white"):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if not 60 <= strip_height <= 120:
        raise ValueError("cleanup strip must stay bounded")
    if color not in {"white", "black"}:
        raise ValueError("unsupported cleanup color")
    return f"drawbox=x=0:y=0:w=iw:h={strip_height}:color={color}:t=fill"


def release_contract():
    return {
        "zero_cost": True,
        "purpose": "remove_internal_top_edge_labels",
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "rights_check_required": True,
        "auto_post": False,
    }
