"""Review-only MP4 checks shared by all ten genres. Requires ffprobe and ffmpeg."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    duration = float(data["format"]["duration"])
    decode = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
                            capture_output=True, text=True)
    return {
        "width": video.get("width") if video else None,
        "height": video.get("height") if video else None,
        "duration": duration,
        "audio_present": audio is not None,
        "decode_ok": decode.returncode == 0,
        "review_only": True,
        "publication_approved": False,
    }

def gate(report, require_audio=True, minimum_height=1920):
    return (report["decode_ok"] and report["width"] >= 1080
            and report["height"] >= minimum_height
            and (report["audio_present"] or not require_audio))
