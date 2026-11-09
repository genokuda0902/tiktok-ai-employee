"""Fail-closed MP4 quality gate. Python standard library + ffprobe/ffmpeg only."""
import json
import subprocess
import sys

def inspect(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path], capture_output=True, text=True, check=True)
    data = json.loads(p.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    issues = []
    if video is None:
        issues.append("missing_video")
    elif video.get("width", 0) < 1080 or video.get("height", 0) < 1920:
        issues.append("low_resolution")
    if audio is None:
        issues.append("missing_audio")
    if float(data.get("format", {}).get("duration", 0)) <= 0:
        issues.append("invalid_duration")
    if video:
        decode = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", path, "-f", "null", "-"], capture_output=True, text=True)
        if decode.returncode:
            issues.append("decode_failed")
    return {"approved": not issues, "issues": issues, "video": video is not None, "audio": audio is not None}

if __name__ == "__main__":
    result = inspect(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["approved"] else 1)
