"""Fail-closed media QA for review-only TikTok prototypes (standard library)."""
import json
import subprocess

def inspect(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    info = json.loads(p.stdout)
    videos = [s for s in info["streams"] if s.get("codec_type") == "video"]
    audio = [s for s in info["streams"] if s.get("codec_type") == "audio"]
    duration = float(info["format"]["duration"])
    return {"video_ok": bool(videos) and videos[0].get("width", 0) >= 720 and videos[0].get("height", 0) >= 1280,
            "audio_stream_present": bool(audio), "duration_seconds": duration,
            "japanese_narration_verified": False, "caption_sync_verified": False,
            "asset_rights_approved": False, "employee_approved": False}

def publication_allowed(report):
    required = ("video_ok", "audio_stream_present", "japanese_narration_verified", "caption_sync_verified", "asset_rights_approved", "employee_approved")
    return all(report.get(k) is True for k in required)
