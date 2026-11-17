"""Fail-closed review-only media QA. Requires ffprobe, no paid services."""
import json
import subprocess
from pathlib import Path

def inspect(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    meta = json.loads(p.stdout)
    streams = meta.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    return {"width": video.get("width"), "height": video.get("height"),
            "duration": float(meta.get("format", {}).get("duration", 0)),
            "has_audio_stream": audio is not None,
            "narration_verified": False,
            "caption_sync_verified": False,
            "rights_approved": False,
            "employee_approved": False,
            "publication_approved": False}

def gate(report):
    # Audio stream existence never proves intelligible Japanese speech.
    return all(report.get(k) is True for k in
               ("narration_verified", "caption_sync_verified", "rights_approved", "employee_approved")) and bool(report.get("has_audio_stream"))

if __name__ == "__main__":
    import sys
    report = inspect(sys.argv[1])
    report["publication_approved"] = gate(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["publication_approved"] else 2)
