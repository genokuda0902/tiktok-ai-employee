"""Fail-closed delivery QA for all genres; standard-library only."""
import json
import subprocess
from pathlib import Path

def inspect(mp4, captions=None, narration_verified=False, rights_approved=False, employee_approved=False):
    mp4 = Path(mp4)
    if not mp4.is_file():
        return {"approved": False, "errors": ["mp4_missing"]}
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                             "-of", "json", str(mp4)], capture_output=True, text=True)
    if result.returncode:
        return {"approved": False, "errors": ["ffprobe_failed"]}
    data = json.loads(result.stdout)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    errors = []
    if not video or video.get("width", 0) < 720 or video.get("height", 0) < 1280:
        errors.append("resolution_or_video_missing")
    if not audio:
        errors.append("audio_missing")
    if not narration_verified:
        errors.append("japanese_narration_unverified")
    if not captions or not Path(captions).is_file():
        errors.append("captions_missing")
    if not rights_approved:
        errors.append("rights_unapproved")
    if not employee_approved:
        errors.append("employee_unapproved")
    return {"approved": not errors, "errors": errors,
            "width": video.get("width") if video else None,
            "height": video.get("height") if video else None,
            "audio_present": bool(audio)}

if __name__ == "__main__":
    import sys
    print(json.dumps(inspect(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None),
                     ensure_ascii=False, indent=2))
