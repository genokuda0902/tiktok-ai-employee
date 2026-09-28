"""Zero-cost, genre-independent completion rail for 9:16 image-slide videos."""

def progress_rail_filter(duration: float, width: int = 1080, height: int = 1920) -> str:
    if duration <= 0:
        raise ValueError("duration must be positive")
    if (width, height) != (1080, 1920):
        raise ValueError("only 1080x1920 release geometry is allowed")
    rail_x, rail_y, rail_w, rail_h = 70, 1760, 940, 6
    return (
        f"drawbox=x={rail_x}:y={rail_y}:w={rail_w}:h={rail_h}:color=white@0.18:t=fill,"
        f"drawbox=x={rail_x}:y={rail_y}:w='{rail_w}*min(t/{duration:.3f},1)':"
        f"h={rail_h}:color=white@0.88:t=fill"
    )

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "width": 1080,
        "height": 1920,
        "preserve_audio": True,
        "preserve_burned_captions": True,
        "manual_post_only": True,
        "human_approval_required": True,
        "auto_post": False,
    }
