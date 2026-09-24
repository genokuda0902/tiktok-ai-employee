"""Zero-cost subtle sharpness finish for portrait image-slide videos.

This is intentionally conservative: it is meant to restore text/card edge clarity
lost during scaling/encoding, not to create halos or invent detail.
"""


def ffmpeg_filter(width: int = 1080, height: int = 1920, amount: float = 0.35) -> str:
    if (width, height) != (1080, 1920):
        raise ValueError("portrait delivery must be 1080x1920")
    if not 0.0 < amount <= 0.45:
        raise ValueError("sharpness amount must stay subtle (0, 0.45]")
    return f"unsharp=5:5:{amount:.2f}:3:3:0.0"


def release_contract() -> dict:
    return {
        "zero_cost": True,
        "preserve_audio": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "reference_quality_claim_allowed_without_review": False,
    }
