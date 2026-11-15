"""Fail closed: a sound cue is not verified Japanese speech."""
import json
import subprocess


def inspect(path, japanese_narration_verified=False, subtitle_sync_verified=False, human_approved=False):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    streams = json.loads(p.stdout)["streams"]
    video = next((s for s in streams if s["codec_type"] == "video"), None)
    audio = next((s for s in streams if s["codec_type"] == "audio"), None)
    return {"video_present": video is not None, "audio_present": audio is not None,
            "japanese_narration_verified": bool(japanese_narration_verified),
            "subtitle_sync_verified": bool(subtitle_sync_verified),
            "publication_approved": bool(human_approved and video and audio and japanese_narration_verified and subtitle_sync_verified)}
