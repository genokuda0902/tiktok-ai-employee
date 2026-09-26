"""Zero-cost TikTok UI safe-area master for image-slide renders.

Scales the finished 1080x1920 composition slightly inward and fills the exposed
edge with a blurred copy. This protects baked headlines/captions from edge UI
without changing copy, audio, or posting policy.
"""

def ffmpeg_filter(width=1080, height=1920, inset_scale=0.96, blur_sigma=22):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if not 0.94 <= inset_scale <= 0.98:
        raise ValueError("inset_scale must stay subtle")
    if not 12 <= blur_sigma <= 30:
        raise ValueError("blur_sigma outside safe range")
    fg_w = round(width * inset_scale)
    fg_h = round(height * inset_scale)
    # yuv420p-friendly even dimensions
    fg_w -= fg_w % 2
    fg_h -= fg_h % 2
    return (
        f"split=2[bg][fg];"
        f"[bg]scale={width}:{height},gblur=sigma={blur_sigma}[bg2];"
        f"[fg]scale={fg_w}:{fg_h}:flags=lanczos[fg2];"
        f"[bg2][fg2]overlay=(W-w)/2:(H-h)/2:format=auto"
    )

def release_contract():
    return {
        "zero_cost": True,
        "target": "tiktok_ui_safe_area",
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
