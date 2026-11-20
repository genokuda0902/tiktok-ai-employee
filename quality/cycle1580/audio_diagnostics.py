"""Fail-closed MP4 audio evidence diagnostics for all content genres."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    probe = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True))
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    return {"width": video.get("width"), "height": video.get("height"),
            "duration": float(probe.get("format", {}).get("duration", 0)),
            "audio_stream_count": len(audio), "has_audio": bool(audio),
            "japanese_speech_verified": False, "subtitle_sync_verified": False,
            "publication_approved": False,
            "blockers": (["NO_AUDIO_TRACK"] if not audio else
                         ["JAPANESE_SPEECH_UNVERIFIED"]) + ["SUBTITLE_SYNC_UNVERIFIED", "HUMAN_APPROVAL_MISSING"]}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
