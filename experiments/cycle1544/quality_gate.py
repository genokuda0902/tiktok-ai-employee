"""Fail-closed review-only quality gate for generated MP4s."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    path = Path(path)
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,codec_name,width,height:format=duration",
        "-of", "json", str(path)], capture_output=True, text=True, check=True)
    info = json.loads(result.stdout)
    streams = info.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    video = videos[0] if videos else {}
    return {"video": bool(videos), "audio": bool(audios),
            "width": video.get("width"), "height": video.get("height"),
            "duration": float(info.get("format", {}).get("duration", 0)),
            "japanese_narration_verified": False,
            "caption_sync_verified": False,
            "posting_allowed": False,
            "human_approval_required": True}

def approved(report):
    return bool(report.get("video") and report.get("audio")
        and report.get("japanese_narration_verified")
        and report.get("caption_sync_verified")
        and report.get("asset_rights_verified")
        and report.get("human_approved"))

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
