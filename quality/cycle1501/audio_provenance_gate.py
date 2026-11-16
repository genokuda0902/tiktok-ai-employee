"""Fail-closed audio provenance classification for 10-genre video reviews."""
import json
import subprocess

ALLOWED_ORIGINS = {"synthetic_cues", "original_narration", "licensed_audio"}

def classify(mp4, manifest):
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams",
                            "-of", "json", str(mp4)], capture_output=True, text=True)
    if probe.returncode:
        return {"approved": False, "reason": "probe_failed"}
    streams = json.loads(probe.stdout).get("streams", [])
    if not any(s.get("codec_type") == "video" for s in streams):
        return {"approved": False, "reason": "missing_video"}
    if not any(s.get("codec_type") == "audio" for s in streams):
        return {"approved": False, "reason": "missing_audio"}
    origin = manifest.get("audio_origin")
    if origin not in ALLOWED_ORIGINS:
        return {"approved": False, "reason": "unknown_audio_provenance"}
    if origin != "original_narration":
        return {"approved": False, "reason": "audio_is_not_narration"}
    if not manifest.get("japanese_speech_verified"):
        return {"approved": False, "reason": "japanese_speech_unverified"}
    if not manifest.get("caption_sync_verified"):
        return {"approved": False, "reason": "caption_sync_unverified"}
    if not manifest.get("asset_rights_verified") or not manifest.get("employee_approved"):
        return {"approved": False, "reason": "rights_or_approval_missing"}
    return {"approved": True, "reason": "documented_checks_passed"}
