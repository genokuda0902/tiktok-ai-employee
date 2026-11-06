"""Review-only cross-genre MP4 QA. Audio stream is necessary but not sufficient for narration."""
import json
import subprocess

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
      "format=duration:stream=codec_type,codec_name,width,height", "-of", "json", str(path)],
      capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def review(meta, *, narration_verified=False, captions_synced=False, assets_approved=False, human_approved=False):
    streams = meta.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = any(s.get("codec_type") == "audio" for s in streams)
    checks = {
        "vertical_720p": video.get("width", 0) >= 720 and video.get("height", 0) >= 1280,
        "has_audio_stream": audio,
        "japanese_narration_verified": audio and narration_verified,
        "speech_captions_synced": captions_synced,
        "assets_approved": assets_approved,
        "human_approved": human_approved,
    }
    return {"checks": checks, "publication_approved": all(checks.values())}
