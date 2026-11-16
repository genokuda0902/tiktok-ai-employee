"""Fail-closed review gate: a decodable silent MP4 is not publishable."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(p)], capture_output=True, text=True, check=True)
    streams = json.loads(probe.stdout)["streams"]
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    decoded = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "null", "-"], capture_output=True).returncode == 0
    return {"video": bool(video), "audio": bool(audio), "decoded": decoded,
            "width": video.get("width") if video else None,
            "height": video.get("height") if video else None,
            "japanese_narration_verified": False,
            "speech_caption_sync_verified": False,
            "rights_approved": False,
            "employee_approved": False,
            "publication_approved": False}
