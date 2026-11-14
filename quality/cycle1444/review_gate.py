"""Fail-closed review gate shared across 10 genres. Stdlib only."""
import json
import subprocess
from pathlib import Path

def inspect_video(path: str, japanese_narration_verified: bool = False,
                  employee_approved: bool = False) -> dict:
    p = Path(path)
    if not p.is_file():
        return {"publishable": False, "issues": ["missing_mp4"]}
    info = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-of", "json", str(p)
    ]))
    video = [s for s in info["streams"] if s.get("codec_type") == "video"]
    audio = [s for s in info["streams"] if s.get("codec_type") == "audio"]
    issues = []
    if not video or (video[0].get("width"), video[0].get("height")) != (1080, 1920):
        issues.append("resolution_or_video_missing")
    if not audio:
        issues.append("audio_missing")
    if not japanese_narration_verified:
        issues.append("japanese_narration_unverified")
    if not employee_approved:
        issues.append("employee_approval_missing")
    return {"publishable": not issues, "issues": issues}
