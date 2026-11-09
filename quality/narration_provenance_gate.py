"""Fail closed: an audio stream alone is not proof of Japanese narration."""
import json
import subprocess
from pathlib import Path

def check(mp4, manifest):
    if not Path(mp4).is_file() or not Path(manifest).is_file():
        return {"approved": False, "reason": "missing_file"}
    try:
        data = json.loads(Path(manifest).read_text(encoding="utf-8"))
        streams = json.loads(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(mp4)],
            text=True))["streams"]
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError):
        return {"approved": False, "reason": "invalid_media_or_manifest"}
    if not any(s.get("codec_type") == "video" for s in streams):
        return {"approved": False, "reason": "missing_video"}
    if not any(s.get("codec_type") == "audio" for s in streams):
        return {"approved": False, "reason": "missing_audio"}
    keys = ["narration_language", "narration_source", "narration_text",
            "voice_rights_reviewed", "captions_sync_reviewed", "human_approved"]
    if any(k not in data for k in keys):
        return {"approved": False, "reason": "missing_narration_provenance"}
    if data["narration_language"] != "ja" or not isinstance(data["narration_text"], str) or not data["narration_text"].strip():
        return {"approved": False, "reason": "japanese_narration_unverified"}
    if not all(data[k] is True for k in ["voice_rights_reviewed", "captions_sync_reviewed", "human_approved"]):
        return {"approved": False, "reason": "review_not_complete"}
    return {"approved": True, "reason": "metadata_passed_manual_listening_still_required"}
