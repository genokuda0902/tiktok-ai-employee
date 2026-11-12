"""Strict, reusable ffprobe-based technical QA. Does not certify speech or rights."""
import json
import subprocess
from pathlib import Path

def inspect(path, narration_verified=False, captions_verified=False, rights_approved=False, human_approved=False):
    path = Path(path)
    data = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], text=True))
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    resolution_ok = bool(video and video.get("width") == 1080 and video.get("height") == 1920)
    # AAC track is not evidence of Japanese speech.
    publishable = all((resolution_ok, bool(audio), narration_verified,
                       captions_verified, rights_approved, human_approved))
    return {"resolution_ok": resolution_ok, "audio_track_present": bool(audio),
            "japanese_narration_verified": narration_verified,
            "speech_captions_verified": captions_verified,
            "rights_approved": rights_approved, "human_approved": human_approved,
            "posting_allowed": publishable}
