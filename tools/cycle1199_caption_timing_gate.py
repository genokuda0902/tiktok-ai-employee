"""Review-only SRT timeline gate; independent of video genre. No publication approval."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path

STAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")
def seconds(value: str) -> float:
    match = STAMP.fullmatch(value.strip())
    if not match:
        raise ValueError("invalid SRT timestamp: " + value)
    h, m, s, ms = map(int, match.groups())
    if m > 59 or s > 59:
        raise ValueError("invalid minute or second")
    return h * 3600 + m * 60 + s + ms / 1000

def check_srt(content: str, duration: float, min_display: float = 0.35) -> dict:
    if duration <= 0:
        raise ValueError("duration must be positive")
    blocks = re.split(r"\n\s*\n", content.strip().replace("\r\n", "\n"))
    if not content.strip():
        raise ValueError("missing subtitles")
    prev_end = 0.0
    errors = []
    count = 0
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].strip().isdigit() or " --> " not in lines[1]:
            errors.append(f"block {count+1}: invalid SRT structure")
            continue
        count += 1
        start_text, end_text = lines[1].split(" --> ", 1)
        try:
            start, end = seconds(start_text), seconds(end_text)
        except ValueError as exc:
            errors.append(f"block {count}: {exc}")
            continue
        if start < prev_end - 0.001:
            errors.append(f"block {count}: overlap or out of order")
        if end <= start or end - start < min_display:
            errors.append(f"block {count}: too short")
        if end > duration + 0.05:
            errors.append(f"block {count}: exceeds video duration")
        if not any(line.strip() for line in lines[2:]):
            errors.append(f"block {count}: empty caption")
        prev_end = max(prev_end, end)
    return {"passed": bool(count) and not errors, "cues": count, "errors": errors,
            "note": "Timeline-only; Japanese transcription and spoken-word synchronization require human/ASR verification."}

def probe_duration(path: str) -> float:
    completed = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True)
    return float(completed.stdout.strip())

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("srt")
    args = parser.parse_args()
    result = check_srt(Path(args.srt).read_text(encoding="utf-8-sig"),
                       probe_duration(args.video))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
