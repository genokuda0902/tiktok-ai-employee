"""Fail-closed Japanese narration preflight. Review-only; no automatic posting."""
from pathlib import Path
import json
import subprocess


def inspect(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    return {"video": any(s.get("codec_type") == "video" for s in streams), "audio": any(s.get("codec_type") == "audio" for s in streams), "duration": float(data.get("format", {}).get("duration", 0))}


def posting_allowed(metadata, spoken_japanese_verified=False, subtitle_sync_verified=False, assets_approved=False, employee_approved=False):
    return bool(metadata["video"] and metadata["audio"] and metadata["duration"] > 0 and spoken_japanese_verified and subtitle_sync_verified and assets_approved and employee_approved)
