"""Zero-cost micro-contrast pass for 1080x1920 image-slide masters.

Keeps the treatment deliberately subtle to recover edge definition after image
resizing without inventing detail or changing narration/caption copy.
Human approval and manual posting remain mandatory.
"""

def ffmpeg_filter(width=1080, height=1920, luma_amount=0.22):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if not 0.10 <= float(luma_amount) <= 0.30:
        raise ValueError("micro-contrast amount must stay subtle")
    return f"unsharp=3:3:{float(luma_amount):.2f}:3:3:0.00,format=yuv420p"


def release_contract():
    return {
        "zero_cost": True,
        "purpose": "recover_subtle_edge_definition_after_resize",
        "changes_copy": False,
        "preserve_audio": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
