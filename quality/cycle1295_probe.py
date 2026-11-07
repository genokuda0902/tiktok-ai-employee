"""Fail-closed review-only media probe. Never authorizes posting."""
import json
import subprocess
from pathlib import Path

def probe(path):
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(p)],
        check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    issues = []
    if video is None:
        issues.append("missing_video")
    elif (video.get("width"), video.get("height")) != (1080, 1920):
        issues.append("resolution_not_1080x1920")
    if audio is None:
        issues.append("missing_audio")
    return {"issues": issues, "video": video is not None, "audio": audio is not None,
            "publication_approved": False, "posting_allowed": False,
            "human_approval_required": True}

if __name__ == "__main__":
    import sys
    print(json.dumps(probe(sys.argv[1]), ensure_ascii=False, indent=2))
