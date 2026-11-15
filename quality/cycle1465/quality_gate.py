"""Fail-closed quality gate for review-only videos, reusable across genres."""
import json
import subprocess
import sys

def inspect(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        check=True, capture_output=True, text=True
    )
    probe = json.loads(result.stdout)
    streams = probe["streams"]
    video = next((s for s in streams if s["codec_type"] == "video"), None)
    audio = next((s for s in streams if s["codec_type"] == "audio"), None)
    return {
        "has_video": video is not None,
        "width": video.get("width") if video else None,
        "height": video.get("height") if video else None,
        "has_audio": audio is not None,
        "duration": float(probe["format"]["duration"]),
    }

def approve(metadata):
    required = ("japanese_narration_verified", "spoken_caption_sync_verified",
                "assets_rights_approved", "privacy_review_approved",
                "employee_approved", "manual_post_only")
    return all(metadata.get(k) is True for k in required)

if __name__ == "__main__":
    data = inspect(sys.argv[1])
    print(json.dumps({**data, "publication_approved": False}, ensure_ascii=False))
    # Inspection is not publication approval.
