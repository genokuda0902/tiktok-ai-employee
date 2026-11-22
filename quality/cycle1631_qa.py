"""Fail-closed technical QA for review-only vertical MP4 (not publication approval)."""
import json
import subprocess
import sys
from pathlib import Path

def inspect(path):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    info = json.loads(raw)
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if not video:
        raise ValueError("missing video stream")
    n, d = map(int, video["r_frame_rate"].split("/"))
    return {"width": int(video["width"]), "height": int(video["height"]),
            "fps": n/d, "duration": float(info["format"]["duration"]),
            "audio_present": audio is not None}

def validate(info, narration_verified=False, captions_verified=False, assets_approved=False, employee_approved=False):
    issues = []
    if (info["width"], info["height"]) != (1080, 1920): issues.append("resolution")
    if info["fps"] < 24: issues.append("frame_rate")
    if not info["audio_present"]: issues.append("missing_audio")
    if not narration_verified: issues.append("japanese_narration_unverified")
    if not captions_verified: issues.append("caption_sync_unverified")
    if not assets_approved: issues.append("assets_unapproved")
    if not employee_approved: issues.append("employee_unapproved")
    return issues

if __name__ == "__main__":
    result = inspect(Path(sys.argv[1]))
    result["issues"] = validate(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(bool(result["issues"]))
