"""Fail-closed media QA for all genres. Stdlib + ffprobe only.

Run: python -m unittest discover -s tests -p 'test_cycle1349*.py'
"""
import json
import subprocess


def assess(probe, narration_verified=False, captions_synced=False, rights_approved=False):
    streams = probe.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    issues = []
    if not video or (video.get("width"), video.get("height")) != (1080, 1920):
        issues.append("resolution_or_video_missing")
    if not audio:
        issues.append("audio_missing")
    if not narration_verified:
        issues.append("japanese_narration_unverified")
    if not captions_synced:
        issues.append("speech_caption_sync_unverified")
    if not rights_approved:
        issues.append("asset_rights_unapproved")
    return {"approved_for_publication": not issues, "issues": issues}


def inspect(path, **kwargs):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)])
    return assess(json.loads(raw), **kwargs)
