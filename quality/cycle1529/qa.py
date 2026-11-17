"""Fail-closed QA for review-only videos. Standard library only."""
import json

def evaluate(probe, *, narration_verified=False, subtitles_verified=False,
             rights_approved=False, employee_approved=False):
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    checks = {
        "portrait": video.get("width") == 720 and video.get("height") == 1280,
        "h264": video.get("codec_name") == "h264",
        "audio_stream": audio is not None,
        "japanese_narration_verified": bool(narration_verified) and audio is not None,
        "synchronized_subtitles_verified": bool(subtitles_verified),
        "rights_approved": bool(rights_approved),
        "employee_approved": bool(employee_approved),
    }
    return {"checks": checks, "publication_approved": all(checks.values())}
