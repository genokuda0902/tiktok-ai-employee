"""Genre-independent first-second hook emphasis for portrait image-slide videos.

Adds a subtle temporary luminance/contrast lift only during the opening hook window.
It does not change caption copy or audio and keeps manual human approval mandatory.
"""


def ffmpeg_filter(window_s: float = 1.6, contrast: float = 1.035, brightness: float = 0.008) -> str:
    if not (0.8 <= window_s <= 2.0):
        raise ValueError("hook window must be 0.8-2.0 seconds")
    if not (1.0 <= contrast <= 1.05):
        raise ValueError("contrast lift must stay subtle")
    if not (0.0 <= brightness <= 0.012):
        raise ValueError("brightness lift must stay subtle")
    return f"eq=contrast={contrast}:brightness={brightness}:enable='between(t,0,{window_s})'"


def output_contract(width: int = 1080, height: int = 1920) -> dict:
    if (width, height) != (1080, 1920):
        raise ValueError("delivery geometry must be 1080x1920")
    return {
        "width": width,
        "height": height,
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "zero_cost": True,
        "human_approval_required": True,
        "auto_post": False,
    }
