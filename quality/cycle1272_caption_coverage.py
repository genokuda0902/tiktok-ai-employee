"""Fail-closed review of scene-timed SRT coverage. Not speech alignment."""
import re
from pathlib import Path

TIME = re.compile(r"^(\d\d):(\d\d):(\d\d),(\d{3})$")

def milliseconds(value):
    match = TIME.fullmatch(value)
    if not match:
        raise ValueError("invalid SRT timestamp")
    h, m, s, ms = map(int, match.groups())
    if m > 59 or s > 59:
        raise ValueError("invalid timestamp range")
    return ((h * 60 + m) * 60 + s) * 1000 + ms

def check_scene_captions(srt_text, duration_ms, max_gap_ms=100):
    blocks = [b.strip().splitlines() for b in re.split(r"\n\s*\n", srt_text.strip()) if b.strip()]
    if not blocks or duration_ms <= 0:
        return False
    previous = 0
    for number, lines in enumerate(blocks, 1):
        if len(lines) < 3 or lines[0] != str(number) or " --> " not in lines[1]:
            return False
        start, end = (milliseconds(x) for x in lines[1].split(" --> "))
        if start < previous or start - previous > max_gap_ms or end <= start or not any(x.strip() for x in lines[2:]):
            return False
        previous = end
    return abs(duration_ms - previous) <= max_gap_ms

def publication_ready(*, caption_coverage, japanese_narration_verified, speech_sync_verified, assets_approved, employee_approved):
    return all((caption_coverage, japanese_narration_verified, speech_sync_verified, assets_approved, employee_approved))
