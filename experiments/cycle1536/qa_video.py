"""Fail-closed MP4 technical QA. This does not approve publication."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError("MP4 missing or empty")
    probe = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]))
    streams = probe["streams"]
    video = next((s for s in streams if s["codec_type"] == "video"), None)
    audio = next((s for s in streams if s["codec_type"] == "audio"), None)
    if not video or video["codec_name"] != "h264" or video["width"] != 720 or video["height"] != 1280:
        raise ValueError("Unexpected video stream")
    subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"], check=True)
    return {"video_decodes": True, "audio_present": bool(audio),
            "japanese_speech_verified": False, "caption_sync_verified": False,
            "rights_verified": False, "human_approved": False,
            "publication_approved": False}
