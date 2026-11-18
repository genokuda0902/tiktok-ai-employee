"""Fail-closed technical review of a generated TikTok MP4. Not publication approval."""
import json
import subprocess
import sys

def inspect(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    checks = {
        "portrait_1080x1920": bool(video and video.get("width") == 1080 and video.get("height") == 1920),
        "h264": bool(video and video.get("codec_name") == "h264"),
        "duration_5_to_60_seconds": 5 <= float(data["format"].get("duration", 0)) <= 60,
        "audio_track_present": audio is not None,
        "japanese_narration_verified": False,
        "speech_caption_sync_verified": False,
        "rights_approved": False,
        "employee_approved": False,
    }
    return {"checks": checks, "publication_approved": all(checks.values())}

if __name__ == "__main__":
    report = inspect(sys.argv[1])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report["publication_approved"] else 2)
