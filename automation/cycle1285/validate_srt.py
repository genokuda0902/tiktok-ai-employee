#!/usr/bin/env python3
"""Fail closed on subtitle timing/coverage. Standard library only."""
import argparse
import re
from pathlib import Path

STAMP = re.compile(r"^(\\d{2}):(\\d{2}):(\\d{2})[,.](\\d{3})$")
def seconds(s):
    m = STAMP.fullmatch(s.strip())
    if not m: raise ValueError("invalid SRT timestamp: " + s)
    h, minute, sec, ms = map(int, m.groups())
    if minute >= 60 or sec >= 60: raise ValueError("timestamp out of range")
    return h * 3600 + minute * 60 + sec + ms / 1000

def validate(srt, duration, expected=8, min_gap=0.0):
    blocks = re.split(r"\\n\\s*\\n", srt.strip())
    if len(blocks) != expected: raise ValueError(f"expected {expected} cues, got {len(blocks)}")
    previous = 0.0
    for n, block in enumerate(blocks, 1):
        lines = block.strip().splitlines()
        if len(lines) < 3 or lines[0].strip() != str(n):
            raise ValueError(f"cue {n}: missing sequence number or text")
        if "-->" not in lines[1]: raise ValueError(f"cue {n}: no time range")
        start, end = [seconds(x) for x in lines[1].split("-->")]
        if start < previous + (min_gap if n > 1 else 0):
            raise ValueError(f"cue {n}: overlap or out-of-order")
        if end <= start or end > duration + 0.001:
            raise ValueError(f"cue {n}: invalid end")
        if not "".join(lines[2:]).strip():
            raise ValueError(f"cue {n}: empty text")
        previous = end
    return True

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("srt", type=Path)
    p.add_argument("--duration", type=float, required=True)
    p.add_argument("--expected", type=int, default=8)
    args = p.parse_args()
    validate(args.srt.read_text(encoding="utf-8-sig"), args.duration, args.expected)
    print("PASS: SRT timing/structure; narration semantic match NOT checked")
