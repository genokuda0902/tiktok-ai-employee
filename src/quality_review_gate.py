"""Reusable review-only MP4 validator; fails closed for publication."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    path = Path(path)
    if not path.is_file():
        return {"ok": False, "issues": ["missing_file"]}
    try:
        data = json.loads(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_streams", "-show_format",
             "-of", "json", str(path)], stderr=subprocess.STDOUT))
        streams = data.get("streams", [])
        video = next((s for s in streams if s.get("codec_type") == "video"), None)
        audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
        issues = []
        if not video: issues.append("missing_video")
        elif (video.get("width"), video.get("height")) != (1080, 1920):
            issues.append("not_1080x1920")
        if not audio: issues.append("missing_narration_audio")
        duration = float(data.get("format", {}).get("duration", 0))
        if not 15 <= duration <= 45: issues.append("duration_outside_target")
        decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path),
                                 "-f", "null", "-"], capture_output=True)
        if decode.returncode: issues.append("decode_failure")
        return {"ok": not issues, "issues": issues, "duration": duration}
    except (OSError, ValueError, subprocess.CalledProcessError):
        return {"ok": False, "issues": ["probe_failure"]}
