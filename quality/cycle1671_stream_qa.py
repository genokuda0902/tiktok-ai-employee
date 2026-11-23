"""Reusable, fail-closed MP4 stream QA for all ten genres. No external services."""
import json
import subprocess
from pathlib import Path

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams",
        "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def inspect(path, narration_verified=False, subtitles_verified=False,
            assets_approved=False, employee_approved=False):
    data = probe(path)
    streams = data.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    dimensions_ok = bool(videos) and videos[0].get("width") == 1080 and videos[0].get("height") == 1920
    # An audio stream alone never proves Japanese speech.
    checks = {"vertical_1080p": dimensions_ok, "audio_stream": bool(audio),
        "japanese_narration_verified": bool(audio) and narration_verified,
        "speech_captions_verified": bool(audio) and subtitles_verified,
        "assets_approved": assets_approved, "employee_approved": employee_approved}
    return {"publishable": all(checks.values()), "checks": checks}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(Path(sys.argv[1])), ensure_ascii=False, indent=2))
