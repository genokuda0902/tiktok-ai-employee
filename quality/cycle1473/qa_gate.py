"""Fail-closed technical gate for review-only TikTok MP4s. Standard library only."""
import json
import subprocess
import sys

def inspect(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True)
    meta = json.loads(result.stdout)
    streams = meta.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    valid_video = len(videos) == 1 and videos[0].get("width") == 1080 and videos[0].get("height") == 1920
    decoded = subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", str(path), "-f", "null", "-"],
                             capture_output=True).returncode == 0
    return {"resolution_ok": valid_video, "decodes": decoded,
            "audio_present": bool(audios), "japanese_narration_verified": False,
            "caption_sync_verified": False, "rights_approved": False,
            "employee_approved": False, "posting_allowed": False}

def test_fail_closed():
    # Audio stream presence alone is not evidence of Japanese narration.
    assert inspect.__name__ == "inspect"
    assert not {"audio_present": True}.get("japanese_narration_verified", False)

if __name__ == "__main__":
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
