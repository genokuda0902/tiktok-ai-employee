"""Fail-closed media verification for all ten TikTok content genres."""
import json
import subprocess
import sys

def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format",
         "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def assess(metadata, narration_verified=False, captions_synced=False,
           assets_approved=False, employee_approved=False):
    streams = metadata.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    failures = []
    if not videos or videos[0].get("width", 0) < 1080 or videos[0].get("height", 0) < 1920:
        failures.append("resolution_or_video_missing")
    if not audios:
        failures.append("audio_stream_missing")
    if not narration_verified:
        failures.append("japanese_narration_unverified")
    if not captions_synced:
        failures.append("caption_sync_unverified")
    if not assets_approved:
        failures.append("asset_rights_unapproved")
    if not employee_approved:
        failures.append("employee_approval_missing")
    return {"posting_allowed": not failures, "failures": failures}

if __name__ == "__main__":
    report = assess(probe(sys.argv[1]))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["posting_allowed"] else 2)
