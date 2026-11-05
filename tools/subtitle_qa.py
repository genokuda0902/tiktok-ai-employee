"""Fail-closed SRT timing and mobile readability checks (stdlib only)."""
import argparse
import json
import re
from pathlib import Path

STAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")
TIMING = re.compile(r"^(.+?) --> (.+?)$")

def millis(value):
    match = STAMP.fullmatch(value.strip())
    if not match:
        raise ValueError(f"invalid SRT timestamp: {value!r}")
    h, m, s, ms = map(int, match.groups())
    if m >= 60 or s >= 60:
        raise ValueError("invalid timestamp range")
    return ((h * 60 + m) * 60 + s) * 1000 + ms

def validate_srt(content, duration_ms, max_chars=18, max_lines=2):
    errors = []
    previous_end = 0
    cues = 0
    for block in re.split(r"\n\s*\n", content.strip().replace("\r\n", "\n")):
        lines = block.splitlines()
        if not lines:
            continue
        if lines[0].strip().isdigit():
            lines = lines[1:]
        if len(lines) < 2:
            errors.append(f"cue {cues + 1}: missing timing or text")
            continue
        timing = TIMING.fullmatch(lines[0].strip())
        if not timing:
            errors.append(f"cue {cues + 1}: invalid timing")
            continue
        try:
            start, end = millis(timing.group(1)), millis(timing.group(2))
        except ValueError as exc:
            errors.append(f"cue {cues + 1}: {exc}")
            continue
        cues += 1
        if start < previous_end:
            errors.append(f"cue {cues}: overlaps previous cue")
        if end <= start:
            errors.append(f"cue {cues}: nonpositive duration")
        if end > duration_ms:
            errors.append(f"cue {cues}: exceeds video duration")
        if len(lines[1:]) > max_lines:
            errors.append(f"cue {cues}: too many lines")
        if any(len(line) > max_chars for line in lines[1:]):
            errors.append(f"cue {cues}: line too long")
        previous_end = max(previous_end, end)
    if not cues:
        errors.append("no valid cues")
    return {"passed": not errors, "cues": cues, "errors": errors,
            "speech_alignment_verified": False,
            "note": "Timing/layout checks do not verify spoken Japanese or audio synchronization."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("srt", type=Path)
    parser.add_argument("--duration-ms", type=int, required=True)
    parser.add_argument("--max-chars", type=int, default=18)
    args = parser.parse_args()
    if args.duration_ms <= 0:
        parser.error("--duration-ms must be positive")
    result = validate_srt(args.srt.read_text(encoding="utf-8-sig"), args.duration_ms, args.max_chars)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)

if __name__ == "__main__":
    main()
