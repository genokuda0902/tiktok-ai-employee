"""Offline-first audio readiness: diagnostics only, not proof of Japanese narration."""
import json
import shutil
import subprocess

def probe_media(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    streams = json.loads(p.stdout).get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    return {"video_present": video is not None, "audio_present": audio is not None,
            "width": video.get("width") if video else None, "height": video.get("height") if video else None,
            "japanese_speech_verified": False, "speech_synced_captions_verified": False}

def diagnose_engines():
    return {"ffmpeg": bool(shutil.which("ffmpeg")), "ffprobe": bool(shutil.which("ffprobe")),
            "espeak_ng": bool(shutil.which("espeak-ng")), "piper": bool(shutil.which("piper")),
            "voicevox": bool(shutil.which("voicevox")),
            "note": "Binary presence does not establish a Japanese voice model or usable narration."}

def publication_allowed(qa):
    return all(qa.get(k) is True for k in ("video_present", "audio_present", "japanese_speech_verified",
                                         "speech_synced_captions_verified", "asset_rights_approved",
                                         "employee_approved"))
