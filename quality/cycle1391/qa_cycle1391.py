"""Reusable fail-closed QA for all 10 content genres."""
import json
import subprocess
from pathlib import Path

def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def evaluate(path, narration_required=True):
    data = probe(path)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    issues = []
    if not video:
        issues.append("missing_video")
    elif (video.get("width"), video.get("height")) != (1080, 1920):
        issues.append("not_1080x1920")
    if narration_required and not audio:
        issues.append("missing_narration")
    return {"approved": not issues, "issues": issues, "audio_tracks": len(audio)}
