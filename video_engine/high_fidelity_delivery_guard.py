"""Fail-closed verification for zero-cost 1080x1920 image-slide delivery masters.

This guard is intentionally genre-independent. It verifies the technical contract
for the high-quality image-slide + Japanese narration + burned captions route.
It never approves content/rights and never posts automatically.
"""


def verify_delivery_probe(probe: dict) -> dict:
    video = probe.get("video") or {}
    audio = probe.get("audio") or {}
    duration = float(probe.get("duration", 0))

    if (video.get("width"), video.get("height")) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    if video.get("codec_name") != "h264" or video.get("pix_fmt") != "yuv420p":
        raise ValueError("delivery must be H.264 yuv420p")
    if video.get("r_frame_rate") != "30/1":
        raise ValueError("delivery must be 30 fps")
    if audio.get("codec_name") != "aac":
        raise ValueError("Japanese narration audio must be AAC")
    if int(audio.get("sample_rate", 0)) != 48000 or int(audio.get("channels", 0)) != 2:
        raise ValueError("audio must be 48 kHz stereo")
    if duration <= 0:
        raise ValueError("duration must be positive")

    return {
        "technical_delivery_ok": True,
        "human_quality_approval_required": True,
        "rights_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "publish_ready_claim_allowed": False,
        "zero_cost": True,
    }
