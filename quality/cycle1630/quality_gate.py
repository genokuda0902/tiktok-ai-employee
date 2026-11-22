"""Review-only quality gate; stream existence is not speech verification."""
import json
import subprocess
from pathlib import Path

def inspect(path, narration_verified=False, captions_synced=False, assets_approved=False, employee_approved=False):
    p = Path(path)
    if not p.is_file():
        return {"posting_allowed": False, "reason": "missing_mp4"}
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(p)], capture_output=True, text=True)
    if result.returncode:
        return {"posting_allowed": False, "reason": "ffprobe_failed"}
    data = json.loads(result.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    reasons = []
    if not video or video.get("width", 0) < 720 or video.get("height", 0) < 1280:
        reasons.append("video_resolution")
    if not audio:
        reasons.append("audio_missing")
    if not narration_verified:
        reasons.append("japanese_narration_unverified")
    if not captions_synced:
        reasons.append("captions_unsynced")
    if not assets_approved:
        reasons.append("asset_rights_unapproved")
    if not employee_approved:
        reasons.append("employee_approval_missing")
    return {"posting_allowed": not reasons, "reasons": reasons, "width": video.get("width") if video else None, "height": video.get("height") if video else None}
