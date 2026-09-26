"""Fail-closed guard against blurred/inset borders on image-slide masters.

The previous safe-area experiment reduced usable visual area by scaling the entire
finished frame inward over a blurred duplicate. For image-first TikTok cards this
can visibly look like a framed repost. This guard keeps the final master full-bleed
while preserving the existing approved composition, audio, captions and manual
release policy.
"""

def release_contract(width=1080, height=1920, full_bleed=True):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if full_bleed is not True:
        raise ValueError("final image-slide master must remain full-bleed")
    return {
        "zero_cost": True,
        "full_bleed_required": True,
        "whole_frame_inset_forbidden": True,
        "blurred_border_forbidden": True,
        "preserve_audio": True,
        "preserve_burned_captions": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }

def ffmpeg_filter(width=1080, height=1920):
    release_contract(width, height, True)
    return "null"
