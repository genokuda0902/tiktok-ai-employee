"""Fail-closed media QA for review renders. Python stdlib only."""
import json
import subprocess
from pathlib import Path

def inspect(path, minimum_height=1920):
    path = Path(path)
    if not path.is_file():
        return {"approved": False, "issues": ["missing_file"]}
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams",
                            "-show_format", "-of", "json", str(path)],
                           capture_output=True, text=True)
    if probe.returncode:
        return {"approved": False, "issues": ["probe_failed"]}
    data = json.loads(probe.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    issues = []
    if not video: issues.append("missing_video")
    if video.get("height", 0) < minimum_height: issues.append("low_resolution")
    if not audio: issues.append("missing_audio")
    decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path),
                             "-f", "null", "-"], capture_output=True)
    if decode.returncode: issues.append("decode_failed")
    return {"approved": not issues, "issues": issues,
            "width": video.get("width"), "height": video.get("height"),
            "duration": data.get("format", {}).get("duration"),
            "audio_codec": audio.get("codec_name")}
