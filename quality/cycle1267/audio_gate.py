"""Fail-closed publication QA. An audio stream alone does not prove Japanese narration."""
import json
import subprocess

def probe(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)["streams"]

def publication_gate(streams, *, japanese_voice_verified=False, captions_synced=False, assets_approved=False, human_approved=False):
    failures = []
    if not any(s.get("codec_type") == "video" for s in streams):
        failures.append("missing_video")
    if not any(s.get("codec_type") == "audio" for s in streams):
        failures.append("missing_audio")
    if not japanese_voice_verified:
        failures.append("japanese_voice_unverified")
    if not captions_synced:
        failures.append("caption_sync_unverified")
    if not assets_approved:
        failures.append("assets_unapproved")
    if not human_approved:
        failures.append("human_approval_missing")
    return failures
