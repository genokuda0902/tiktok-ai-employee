"""Fail-closed media QA for review-only TikTok drafts (stdlib only)."""
import json
import subprocess
from pathlib import Path

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def validate(path, narration_verified=False, captions_synced=False, rights_approved=False, employee_approved=False):
    data = probe(path)
    streams = data.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    reasons = []
    if len(videos) != 1 or videos[0].get("width", 0) < 720 or videos[0].get("height", 0) < 1280:
        reasons.append("vertical_resolution_or_video_missing")
    if not audio or not narration_verified:
        reasons.append("japanese_narration_not_verified")
    if not captions_synced:
        reasons.append("caption_sync_not_verified")
    if not rights_approved:
        reasons.append("rights_not_approved")
    if not employee_approved:
        reasons.append("employee_approval_missing")
    return {"posting_allowed": not reasons, "reasons": reasons, "review_only": bool(reasons)}

if __name__ == "__main__":
    import sys
    print(json.dumps(validate(Path(sys.argv[1])), ensure_ascii=False, indent=2))
