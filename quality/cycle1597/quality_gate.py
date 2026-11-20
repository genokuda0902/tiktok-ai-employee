"""Reject review videos lacking Japanese narration; shared across ten genres."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams",
        "-show_format", "-of", "json", str(path)], text=True)
    info = json.loads(raw)
    videos = [s for s in info["streams"] if s["codec_type"] == "video"]
    audio = [s for s in info["streams"] if s["codec_type"] == "audio"]
    reasons = []
    if not videos or (videos[0].get("width"), videos[0].get("height")) != (720, 1280):
        reasons.append("invalid_vertical_video")
    if not audio:
        reasons.append("missing_japanese_narration")
    # An audio stream alone is not proof of Japanese speech or subtitle alignment.
    reasons.extend(["speech_language_unverified", "subtitle_alignment_unverified",
                    "asset_approval_unverified", "employee_approval_missing"])
    return {"publishable": not reasons, "reasons": reasons,
            "duration": float(info["format"]["duration"])}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(Path(sys.argv[1])), ensure_ascii=False, indent=2))
