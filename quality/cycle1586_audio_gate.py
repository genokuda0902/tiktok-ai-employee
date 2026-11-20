"""Reusable QA for review-only vertical MP4s. Fail closed on absent Japanese narration."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    data = json.loads(raw)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = [s for s in data["streams"] if s["codec_type"] == "audio"]
    return {"width": video.get("width") if video else None,
            "height": video.get("height") if video else None,
            "duration": float(data["format"].get("duration", 0)),
            "audio_streams": len(audio),
            "japanese_speech_verified": False,
            "publish_approved": False}

def publishable(result, speech_evidence=False, synced_captions=False, asset_approved=False, employee_approved=False):
    return bool(result["width"] and result["height"] and result["audio_streams"] and speech_evidence and synced_captions and asset_approved and employee_approved)
