"""Subtle caption-focus treatment for the image-first TikTok route."""


def caption_focus_filter(width=1080, height=1920, panel_y=1460, panel_h=230, opacity=0.18):
    if (width, height) != (1080, 1920):
        raise ValueError("portrait delivery must be 1080x1920")
    if not 0.10 <= opacity <= 0.20:
        raise ValueError("caption focus opacity must remain subtle")
    if panel_y < 0 or panel_h <= 0 or panel_y + panel_h > height:
        raise ValueError("caption focus panel outside frame")
    return f"drawbox=x=0:y={panel_y}:w={width}:h={panel_h}:color=black@{opacity}:t=fill"


def release_contract():
    return {
        "zero_cost": True,
        "image_first": True,
        "preserve_narration": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
