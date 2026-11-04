"""Fail-closed media QA for all genres. Stdlib only; ffprobe required."""
import json
import subprocess
from pathlib import Path

def probe(path, runner=subprocess.run):
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError("MP4 missing or empty")
    p = runner(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
               capture_output=True, text=True, check=True)
    return json.loads(p.stdout)

def evaluate(meta, *, captions_verified=False, japanese_speech_verified=False,
             privacy_approved=False, visual_reviewed=False):
    streams = meta.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = float(meta.get("format", {}).get("duration", 0))
    checks = {
        "portrait_1080x1920": bool(video and video.get("width") == 1080 and video.get("height") == 1920),
        "h264_video": bool(video and video.get("codec_name") == "h264"),
        "audio_present": bool(audio),
        "duration_20_to_45s": 20 <= duration <= 45,
        "japanese_speech_verified": bool(japanese_speech_verified),
        "captions_synced_verified": bool(captions_verified),
        "visual_reviewed": bool(visual_reviewed),
        "privacy_and_rights_approved": bool(privacy_approved),
    }
    return {"status": "PASS" if all(checks.values()) else "REVIEW_REQUIRED",
            "checks": checks, "duration_seconds": duration,
            "note": "Audio stream presence does not prove Japanese speech or synchronization."}

def check_file(path, **kwargs):
    return evaluate(probe(path), **kwargs)
