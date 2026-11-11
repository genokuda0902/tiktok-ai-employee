"""Fail-closed QA for review-only videos. No publication authorization is inferred."""
import json
import subprocess
from pathlib import Path

def probe(path):
    return json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True))

def assess(path, manifest):
    data = probe(path)
    streams = data["streams"]
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    problems = []
    if not video or video.get("width") != 1080 or video.get("height") != 1920:
        problems.append("target_resolution_unverified")
    if not audio:
        problems.append("audio_missing")
    if not manifest.get("narration_verified", False):
        problems.append("japanese_narration_unverified")
    if not manifest.get("captions_synced", False):
        problems.append("captions_unsynchronized")
    if not manifest.get("approved", False):
        problems.append("human_approval_missing")
    return {"posting_allowed": not problems, "issues": problems,
            "duration": float(data["format"]["duration"]),
            "audio_codec": audio.get("codec_name") if audio else None}

if __name__ == "__main__":
    import sys
    result = assess(Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["posting_allowed"] else 2)
