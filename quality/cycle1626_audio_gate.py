"""Fail-closed media stream validation for review-only TikTok renders."""
import json
import subprocess
from pathlib import Path

def probe(path: str) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def assess(media: dict, *, japanese_speech_verified=False,
           captions_synced=False, assets_approved=False,
           employee_approved=False) -> dict:
    streams = media.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    duration = float(media.get("format", {}).get("duration") or 0)
    valid_video = bool(videos) and all(
        s.get("width", 0) >= 720 and s.get("height", 0) >= 1280
        for s in videos)
    checks = {
        "video": valid_video,
        "duration": 5 <= duration <= 60,
        "audio_stream": bool(audio),
        "japanese_speech_verified": japanese_speech_verified,
        "captions_synced": captions_synced,
        "assets_approved": assets_approved,
        "employee_approved": employee_approved,
    }
    return {"checks": checks, "posting_allowed": all(checks.values()),
            "status": "PUBLICATION_APPROVED" if all(checks.values()) else "PUBLICATION_NOT_APPROVED"}

def check_file(path: str) -> dict:
    if not Path(path).is_file():
        raise FileNotFoundError(path)
    return assess(probe(path))
