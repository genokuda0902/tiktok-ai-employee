"""Fail-closed timed-caption QA for review-only videos (stdlib only)."""
from dataclasses import dataclass
import re

TIME = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")

def milliseconds(value):
    match = TIME.fullmatch(value)
    if not match:
        raise ValueError("invalid SRT timestamp")
    h, m, s, ms = map(int, match.groups())
    if m >= 60 or s >= 60:
        raise ValueError("invalid clock")
    return ((h * 60 + m) * 60 + s) * 1000 + ms

def validate_srt(srt, duration_ms, *, narration_verified=False):
    """No claim of spoken-word sync without independently verified narration."""
    if duration_ms <= 0:
        raise ValueError("invalid duration")
    blocks = re.split(r"\n\s*\n", srt.strip())
    previous_end = 0
    for index, block in enumerate(blocks, 1):
        lines = block.strip().splitlines()
        if len(lines) < 3 or lines[0].strip() != str(index):
            raise ValueError("missing or out-of-order caption")
        times = lines[1].split(" --> ")
        if len(times) != 2 or not any(line.strip() for line in lines[2:]):
            raise ValueError("empty caption or bad time range")
        start, end = map(milliseconds, times)
        if start < previous_end or end <= start or end > duration_ms:
            raise ValueError("overlap, reversed caption, or exceeds video")
        previous_end = end
    return {"caption_blocks": len(blocks), "timing_valid": True,
            "narration_verified": bool(narration_verified),
            "speech_sync_verified": False, "posting_allowed": False}
