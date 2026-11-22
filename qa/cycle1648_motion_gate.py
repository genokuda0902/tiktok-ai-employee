"""Reusable review-only QA gate for all ten genres. No publishing authority."""
import json
import subprocess
from pathlib import Path

def probe(path):
    return json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True))

def evaluate(metadata, *, captions_timed=False, japanese_speech_verified=False,
             asset_rights_approved=False, employee_approved=False):
    video = next((s for s in metadata.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = next((s for s in metadata.get("streams", []) if s.get("codec_type") == "audio"), None)
    checks = {
        "portrait_1080": bool(video and video.get("width") == 1080 and video.get("height") == 1920),
        "video_present": video is not None,
        "audio_present": audio is not None,
        "japanese_speech_verified": japanese_speech_verified and audio is not None,
        "captions_timed": captions_timed,
        "asset_rights_approved": asset_rights_approved,
        "employee_approved": employee_approved,
    }
    return {"checks": checks, "posting_allowed": all(checks.values()),
            "quality_status": "APPROVAL_REQUIRED" if all(checks.values()) else "PUBLICATION_NOT_APPROVED"}
