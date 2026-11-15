"""Fail-closed review QA. Does not certify Japanese speech from an audio stream."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams",
                             "-show_format", "-of", "json", str(path)],
                            capture_output=True, text=True, check=True)
    info = json.loads(result.stdout)
    streams = info.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    return {
        "video_present": video is not None,
        "width": video.get("width") if video else None,
        "height": video.get("height") if video else None,
        "audio_present": audio is not None,
        "japanese_narration_verified": False,
        "caption_sync_verified": False,
        "human_approved": False,
        "posting_allowed": False,
        "duration": float(info.get("format", {}).get("duration", 0)),
    }

def validate(report):
    return bool(report["video_present"] and report["audio_present"]
                and report["japanese_narration_verified"]
                and report["caption_sync_verified"]
                and report["human_approved"])

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(Path(sys.argv[1])), ensure_ascii=False, indent=2))
