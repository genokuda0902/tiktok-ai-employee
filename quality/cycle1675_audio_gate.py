"""Fail-closed QA for review-only TikTok renders. No publication authorization."""
def evaluate(probe, *, japanese_speech_verified=False, captions_synced=False,
             assets_approved=False, employee_approved=False):
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    checks = {
        "video_present": video is not None,
        "vertical_720_min": bool(video and video.get("width", 0) >= 720 and video.get("height", 0) >= 1280 and video["height"] > video["width"]),
        "audio_present": audio is not None,
        "japanese_speech_verified": bool(japanese_speech_verified),
        "captions_synced": bool(captions_synced),
        "assets_approved": bool(assets_approved),
        "employee_approved": bool(employee_approved),
    }
    return {"checks": checks, "posting_allowed": all(checks.values()), "status": "APPROVED" if all(checks.values()) else "PUBLICATION_NOT_APPROVED"}
