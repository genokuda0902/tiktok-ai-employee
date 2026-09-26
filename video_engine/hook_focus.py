"""Zero-cost opening-hook emphasis for the image-slide route."""


def hook_focus_filter(duration=1.20, contrast=1.04, saturation=1.03):
    if not 0.6 <= duration <= 1.5:
        raise ValueError("hook emphasis must stay between 0.6 and 1.5 seconds")
    if not 1.0 <= contrast <= 1.06:
        raise ValueError("contrast is too aggressive")
    if not 1.0 <= saturation <= 1.05:
        raise ValueError("saturation is too aggressive")
    return (
        f"eq=contrast={contrast:.3f}:saturation={saturation:.3f}:"
        f"enable='between(t,0,{duration:.2f})'"
    )


def release_contract(width=1080, height=1920):
    if (width, height) != (1080, 1920):
        raise ValueError("portrait 1080x1920 required")
    return {
        "zero_cost": True,
        "opening_hook_only": True,
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
