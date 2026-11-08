"""Review-only contract for 10-genre captioned MP4 prototypes."""
import json
import subprocess
from pathlib import Path


def inspect_video(path):
    data = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(path)], text=True))
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    return {"width": video["width"] if video else 0,
            "height": video["height"] if video else 0,
            "duration": float(data["format"]["duration"]),
            "has_audio": audio is not None}


def publication_ready(report, *, timed_captions_verified=False,
                      rights_approved=False, employee_approved=False):
    return (report["width"] >= 1080 and report["height"] >= 1920
            and report["has_audio"] and timed_captions_verified
            and rights_approved and employee_approved)
