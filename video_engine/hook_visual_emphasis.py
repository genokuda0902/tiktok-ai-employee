"""Zero-cost first-second visual emphasis for image-slide videos."""


def hook_visual_filter(duration: float = 0.9) -> str:
    if duration < 0.5 or duration > 1.5:
        raise ValueError("hook emphasis duration must be 0.5..1.5 seconds")
    d = f"{duration:.3f}"
    return (
        "eq="
        f"brightness='if(lt(t,{d}),0.035*(1-t/{d}),0)':"
        f"saturation='if(lt(t,{d}),1.08-0.08*t/{d},1)':eval=frame"
    )


def hook_visual_contract(width: int = 1080, height: int = 1920) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("hook visual emphasis requires 1080x1920")
    return {
        "zero_cost": True,
        "first_second_only": True,
        "changes_caption_copy": False,
        "changes_audio": False,
        "human_approval_required": True,
        "auto_post": False,
    }
