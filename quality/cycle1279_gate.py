"""Fail-closed review gate for generated TikTok MP4 files (10-genre reusable)."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    path = Path(path)
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    issues = []
    if not video: issues.append("missing_video")
    elif (video.get("width"), video.get("height")) != (1080, 1920):
        issues.append("not_1080x1920")
    if not audio: issues.append("missing_narration_audio")
    # Audio-stream existence cannot prove Japanese language or narration quality.
    issues.append("japanese_narration_not_human_verified")
    issues.append("caption_sync_not_human_verified")
    issues.append("asset_rights_not_approved")
    issues.append("employee_approval_missing")
    return {"posting_allowed": False, "status": "REVIEW_ONLY", "issues": issues}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
