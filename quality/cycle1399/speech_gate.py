"""Fail closed: AAC track alone is not proof of spoken Japanese."""
import json
import subprocess

def probe(path):
    return json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True))

def publication_gate(metadata, probe_data):
    streams = probe_data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), {})
    issues = []
    if (video.get("width"), video.get("height")) != (1080, 1920):
        issues.append("resolution")
    if not audio:
        issues.append("audio_track_missing")
    if not metadata.get("japanese_narration_verified", False):
        issues.append("japanese_narration_unverified")
    if not metadata.get("caption_sync_verified", False):
        issues.append("caption_sync_unverified")
    if not metadata.get("asset_rights_approved", False):
        issues.append("asset_rights_unapproved")
    if not metadata.get("employee_approved", False):
        issues.append("employee_approval_missing")
    return {"posting_allowed": not issues, "issues": issues}
