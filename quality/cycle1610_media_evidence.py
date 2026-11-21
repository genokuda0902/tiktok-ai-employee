"""Fail-closed media evidence checks. Does not certify Japanese speech or synchronization."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams",
                        "-show_format", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    obj = json.loads(p.stdout)
    video = next((s for s in obj["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in obj["streams"] if s["codec_type"] == "audio"), None)
    width = int(video.get("width", 0)) if video else 0
    height = int(video.get("height", 0)) if video else 0
    return {"video_present": bool(video), "width": width, "height": height,
            "audio_track_present": bool(audio),
            "japanese_narration_verified": False,
            "speech_caption_sync_verified": False,
            "duration": float(obj.get("format", {}).get("duration", 0))}

def publication_allowed(report, *, asset_approved=False, privacy_approved=False,
                        employee_approved=False):
    return all((report["video_present"], report["width"] >= 720,
                report["height"] >= 1280, report["audio_track_present"],
                report["japanese_narration_verified"],
                report["speech_caption_sync_verified"],
                asset_approved, privacy_approved, employee_approved))
