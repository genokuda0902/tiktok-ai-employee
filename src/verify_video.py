"""Verify actual rendered files; never infer quality from a hard-coded score."""
import json
import subprocess
import sys
from pathlib import Path


def verify(path):
    path = Path(path)
    errors = []
    if not path.is_file() or path.stat().st_size == 0:
        return {"file": str(path), "passed": False, "issues": ["missing_or_empty_video"]}
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
            capture_output=True, text=True, check=True, timeout=30,
        )
        probe = json.loads(result.stdout)
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        return {"file": str(path), "passed": False, "issues": ["probe_failed"], "detail": str(exc)}
    streams = probe.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    if not videos:
        errors.append("video_stream_missing")
    elif any((s.get("width"), s.get("height")) != (1080, 1920) for s in videos):
        errors.append("not_1080x1920")
    if not audios:
        errors.append("audio_stream_missing")
    try:
        duration = float(probe.get("format", {}).get("duration", 0))
    except (TypeError, ValueError):
        duration = 0
    if not 20 <= duration <= 45:
        errors.append("duration_out_of_range")
    return {"file": str(path), "passed": not errors, "issues": errors,
            "observed": {"duration_seconds": duration, "size_bytes": path.stat().st_size,
                         "video_streams": len(videos), "audio_streams": len(audios)}}


if __name__ == "__main__":
    paths = [Path(p) for p in sys.argv[1:]] or sorted(Path("output").glob("*.mp4"))
    report = {"source": "ffprobe", "results": [verify(p) for p in paths]}
    report["passed"] = bool(paths) and all(item["passed"] for item in report["results"])
    Path("output").mkdir(exist_ok=True)
    Path("output/video_verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(0 if report["passed"] else 2)
