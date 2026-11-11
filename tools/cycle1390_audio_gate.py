"""Genre-independent fail-closed MP4 evidence gate. No publication side effects."""
import json
import subprocess
from pathlib import Path


def inspect(path):
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        return {"publishable": False, "reason": "missing_mp4"}
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,width,height:format=duration", "-of", "json", str(path)],
        capture_output=True, text=True)
    if result.returncode:
        return {"publishable": False, "reason": "probe_failed"}
    metadata = json.loads(result.stdout)
    streams = metadata.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    dimensions_ok = bool(videos) and (videos[0].get("width"), videos[0].get("height")) == (1080, 1920)
    return {"publishable": False, "reason": "narration_and_human_approval_unverified",
            "video_ok": dimensions_ok, "audio_track_present": bool(audio),
            "narration_verified": False, "speech_captions_verified": False}
