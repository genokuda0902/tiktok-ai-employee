"""Fail-closed publication gate: an AAC stream is not proof of Japanese speech."""
import json
import subprocess
from pathlib import Path

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                             "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def review(metadata, probe_data):
    streams = probe_data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = any(s.get("codec_type") == "audio" for s in streams)
    reasons = []
    if not video: reasons.append("missing_video")
    if not audio: reasons.append("missing_audio_stream")
    # A tone or music track must never be mistaken for speech.
    if not metadata.get("japanese_speech_verified"): reasons.append("japanese_speech_unverified")
    if not metadata.get("caption_sync_verified"): reasons.append("caption_sync_unverified")
    if not metadata.get("assets_approved"): reasons.append("assets_unapproved")
    if not metadata.get("employee_approved"): reasons.append("employee_unapproved")
    return {"publication_approved": not reasons, "reasons": reasons,
            "width": video.get("width") if video else None,
            "height": video.get("height") if video else None,
            "has_audio_stream": audio}

if __name__ == "__main__":
    import sys
    print(json.dumps(review({}, probe(sys.argv[1])), ensure_ascii=False, indent=2))
