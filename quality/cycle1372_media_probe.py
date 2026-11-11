"""Review-only media probe: codec presence never proves Japanese narration."""
import json, subprocess
from pathlib import Path

def inspect(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    raw = subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)])
    data = json.loads(raw)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    return {"width":video.get("width") if video else None,
            "height":video.get("height") if video else None,
            "duration":float(data["format"]["duration"]),
            "audio_codec":audio.get("codec_name") if audio else None,
            "narration_verified":False, "caption_sync_verified":False,
            "posting_allowed":False, "human_approval_required":True}

def assert_review_only(report):
    assert report["posting_allowed"] is False
    assert report["human_approval_required"] is True
    assert not report["narration_verified"]
    return True
