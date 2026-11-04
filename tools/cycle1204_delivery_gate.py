"""Fail-closed delivery gate for 10 genre video outputs (review only)."""
import argparse
import json
import subprocess
from pathlib import Path


def inspect(video: Path, captions: Path) -> dict:
    errors = []
    if not video.is_file() or video.stat().st_size == 0:
        return {"approved": False, "errors": ["missing_or_empty_mp4"]}
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_streams", "-show_format",
             "-of", "json", str(video)], capture_output=True, text=True,
            check=True, timeout=30)
        probe = json.loads(result.stdout)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired,
            json.JSONDecodeError):
        return {"approved": False, "errors": ["ffprobe_failed"]}
    streams = probe.get("streams", [])
    vids = [s for s in streams if s.get("codec_type") == "video"]
    auds = [s for s in streams if s.get("codec_type") == "audio"]
    if not vids:
        errors.append("missing_video")
    elif (vids[0].get("width"), vids[0].get("height")) != (1080, 1920):
        errors.append("wrong_resolution")
    if not auds:
        errors.append("missing_audio")
    try:
        duration = float(probe.get("format", {}).get("duration", 0))
    except (ValueError, TypeError):
        duration = 0
    if not 10 <= duration <= 90:
        errors.append("invalid_duration")
    if not captions.is_file():
        errors.append("missing_caption_sidecar")
    else:
        try:
            cues = json.loads(captions.read_text(encoding="utf-8"))
            if not isinstance(cues, list) or not cues:
                raise ValueError("empty captions")
            last_end = 0.0
            for cue in cues:
                start, end = float(cue["start"]), float(cue["end"])
                text = cue["text"]
                if (not isinstance(text, str) or not text.strip()
                        or start < last_end or end <= start or end > duration + 0.05):
                    raise ValueError("invalid cue")
                last_end = end
        except (ValueError, TypeError, KeyError, json.JSONDecodeError, UnicodeError):
            errors.append("invalid_caption_timing")
    # Stream presence and cue timestamps do NOT prove Japanese speech or semantic sync.
    return {"approved": False, "technical_gate_pass": not errors,
            "errors": errors, "human_review_required": True,
            "posting_allowed": False, "japanese_speech_verified": False,
            "semantic_sync_verified": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mp4", type=Path)
    parser.add_argument("captions_json", type=Path)
    args = parser.parse_args()
    report = inspect(args.mp4, args.captions_json)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report.get("technical_gate_pass") else 1)


if __name__ == "__main__":
    main()
