"""Fail-closed QA for review-only MP4s; never marks a video publication-ready."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    data = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(p)]
    ))
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    return {
        "width": video["width"] if video else None,
        "height": video["height"] if video else None,
        "duration": float(data["format"]["duration"]),
        "audio_present": audio is not None,
        "japanese_narration_verified": False,
        "caption_sync_verified": False,
        "posting_allowed": False,
        "quality_status": "PUBLICATION_NOT_APPROVED",
    }
