"""Cycle1627: fail-closed QA for review-only demo videos."""
import json
import subprocess
from pathlib import Path

def inspect(path, *, japanese_speech_verified=False, synchronized_captions_verified=False,
            assets_approved=False, employee_approved=False):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,codec_name,width,height:format=duration",
        "-of", "json", str(path)], capture_output=True, text=True, check=True)
    info = json.loads(p.stdout)
    streams = info.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = float(info.get("format", {}).get("duration", 0))
    checks = {
        "video_present": bool(video),
        "vertical_video": video.get("height", 0) > video.get("width", 0),
        "duration_positive": duration > 0,
        "audio_present": audio is not None,
        "japanese_speech_verified": bool(japanese_speech_verified),
        "synchronized_captions_verified": bool(synchronized_captions_verified),
        "assets_approved": bool(assets_approved),
        "employee_approved": bool(employee_approved),
    }
    return {"checks": checks, "posting_allowed": all(checks.values()),
            "status": "APPROVED" if all(checks.values()) else "PUBLICATION_NOT_APPROVED"}
