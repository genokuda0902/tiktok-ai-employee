"""Fail-closed review gate for generated videos. No claim of voice from video-only streams."""

def review_status(video_streams, narration_verified=False, captions_verified=False, assets_approved=False, employee_approved=False):
    has_video = any(s.get("codec_type") == "video" for s in video_streams)
    has_audio = any(s.get("codec_type") == "audio" for s in video_streams)
    checks = dict(video=has_video, audio=has_audio, japanese_narration=bool(narration_verified and has_audio), synchronized_captions=bool(captions_verified), assets=bool(assets_approved), employee=bool(employee_approved))
    return {"checks": checks, "posting_allowed": all(checks.values()), "status": "APPROVED_FOR_MANUAL_POST" if all(checks.values()) else "PUBLICATION_NOT_APPROVED"}
