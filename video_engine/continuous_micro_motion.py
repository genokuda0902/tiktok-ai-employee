"""Zero-cost continuous micro-motion for image-first TikTok slides.

Reimplementation helper: adds very small, slow whole-frame drift to reduce the
static-slide feel while preserving portrait geometry and existing audio/caption
copy. Human approval remains mandatory; this module never posts.
"""


def micro_motion_filter(width=1080, height=1920, overscan=1.012, period=4.0):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if not (1.005 <= overscan <= 1.02):
        raise ValueError("overscan must remain subtle")
    if not (3.0 <= period <= 8.0):
        raise ValueError("motion period outside safe range")
    sw = int(round(width * overscan / 2) * 2)
    sh = int(round(height * overscan / 2) * 2)
    max_x = sw - width
    max_y = sh - height
    # Slow sub-1% drift. No black edges because the source is overscanned first.
    return (
        f"scale={sw}:{sh}:flags=lanczos,"
        f"crop={width}:{height}:"
        f"x='{max_x}/2+({max_x}/3)*sin(2*PI*t/{period:.3f})':"
        f"y='{max_y}/2+({max_y}/3)*cos(2*PI*t/{period*1.35:.3f})'"
    )


def safety_contract():
    return {
        "width": 1080,
        "height": 1920,
        "zero_cost": True,
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "auto_post": False,
        "max_overscan": 1.02,
    }
