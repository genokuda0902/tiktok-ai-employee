"""Cycle1296 reusable review quality gate. No publication authorization."""
import json
import subprocess
from pathlib import Path

def probe(path):
    data = subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], text=True)
    return json.loads(data)

def assess(path, approved_assets=False, approved_by_employee=False, narration_verified=False, captions_synced=False):
    info = probe(path)
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), {})
    audio = any(s["codec_type"] == "audio" for s in info["streams"])
    checks = {
        "portrait_1080p": video.get("width") == 1080 and video.get("height") == 1920,
        "audio_stream": audio,
        "japanese_narration_verified": bool(narration_verified) and audio,
        "captions_synced": bool(captions_synced),
        "approved_assets": bool(approved_assets),
        "employee_approved": bool(approved_by_employee),
    }
    return {"checks": checks, "publication_approved": all(checks.values())}

if __name__ == "__main__":
    import sys
    print(json.dumps(assess(Path(sys.argv[1])), ensure_ascii=False, indent=2))
