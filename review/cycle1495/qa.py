"""Fail-closed video quality gate. Audio presence never proves Japanese speech."""
import json
import subprocess

def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(path)
    ]))

def assess(path, japanese_narration_verified=False,
           captions_synchronized_verified=False,
           rights_approved=False, human_approved=False):
    p = probe(path)
    streams = p["streams"]
    v = next((s for s in streams if s["codec_type"] == "video"), None)
    a = next((s for s in streams if s["codec_type"] == "audio"), None)
    checks = {
        "video": bool(v),
        "vertical_720p": bool(v and v["width"] >= 720 and v["height"] >= 1280 and v["height"] > v["width"]),
        "audio_stream": bool(a),
        "japanese_narration_verified": bool(a and japanese_narration_verified),
        "captions_synchronized_verified": bool(a and captions_synchronized_verified),
        "rights_approved": bool(rights_approved),
        "human_approved": bool(human_approved),
    }
    return {"checks": checks, "publication_approved": all(checks.values()),
            "duration": float(p["format"]["duration"])}
