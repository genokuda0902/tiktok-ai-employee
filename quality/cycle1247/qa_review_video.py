"""Fail-closed media QA for review-only TikTok exports (standard library)."""
import json
import subprocess

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def check_review_media(info):
    streams = info.get("streams", [])
    video = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    if len(video) != 1 or video[0].get("codec_name") != "h264":
        raise ValueError("Exactly one H264 video stream required")
    if (video[0].get("width"), video[0].get("height")) != (1080, 1920):
        raise ValueError("1080x1920 required")
    if not 10 <= float(info["format"]["duration"]) <= 45:
        raise ValueError("Duration outside review bounds")
    return {"review_only": True, "has_audio": bool(audio), "japanese_narration_verified": False, "caption_sync_verified": False, "publication_approved": False}
