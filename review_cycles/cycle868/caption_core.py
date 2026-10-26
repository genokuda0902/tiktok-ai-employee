"""Reusable zero-cost Japanese phrase-highlight subtitle core (review-only).
Input: phrase beats, not phoneme-aligned. 1080x1920 portrait safe zone.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import json
import math
import re

WIDTH, HEIGHT = 1080, 1920
PANEL = (35, 1330, 1010, 285)
CAPTION_CENTER = (540, 1460)
SAFE_LEFT, SAFE_RIGHT = 75, 1020
GENRE_THEMES = {
    "ai_productivity": "#38DCCA", "career": "#FFBB68", "money": "#82DBAA",
    "health": "#87CFFB", "learning": "#BEA7FF", "beauty": "#F4A4C5",
    "travel": "#78C6FA", "food": "#F6B778", "home": "#A5DC8E",
    "business": "#82A9FF",
}

@dataclass(frozen=True)
class Beat:
    start: float
    end: float
    text: str

def load_beats(path: str) -> list[Beat]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    beats = [Beat(float(b["start"]), float(b["end"]), str(b["text"])) for b in raw]
    validate_beats(beats)
    return beats

def validate_beats(beats: Sequence[Beat], *, max_duration: float = 23.034) -> None:
    if not beats:
        raise ValueError("No captions")
    last_end = 0.0
    for b in beats:
        if not (math.isfinite(b.start) and math.isfinite(b.end)):
            raise ValueError("Nonfinite time")
        if b.start < last_end - 0.001 or b.end <= b.start or b.end > max_duration + 0.01:
            raise ValueError("Out of order / out of bounds caption")
        if not b.text or len(b.text) > 18 or re.search(r"[{}\\\r\n]", b.text):
            raise ValueError("Caption too long or unsafe for ASS")
        last_end = b.end
    x, y, w, h = PANEL
    assert 0 < x < x + w < WIDTH
    assert 0 < y < y + h < HEIGHT - 300
    assert SAFE_LEFT < CAPTION_CENTER[0] < SAFE_RIGHT

def ass_time(seconds: float) -> str:
    total = round(seconds * 100)
    h, rem = divmod(total, 360000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def karaoke_tags(text: str, duration: float) -> str:
    # Equal per-character timing is aesthetic, NOT phoneme alignment.
    n = len(text)
    total_cs = max(n, round(duration * 100))
    q, r = divmod(total_cs, n)
    return "".join(f"{{\\kf{q + (1 if i < r else 0)}}}{char}" for i, char in enumerate(text))

def build_ass(beats: Sequence[Beat], *, genre: str = "ai_productivity") -> str:
    validate_beats(beats)
    if genre not in GENRE_THEMES:
        raise ValueError("Unknown genre")
    header = """[Script Info]
Title: cycle868 Japanese phrase highlight - HUMAN REVIEW
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Highlight,Noto Sans CJK JP,64,&H0066E8FF,&H00FFFFFF,&H0005151F,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for b in beats:
        payload = karaoke_tags(b.text, b.end - b.start)
        lines.append(f"Dialogue: 0,{ass_time(b.start)},{ass_time(b.end)},Highlight,,0,0,0,,{{\\pos({CAPTION_CENTER[0]},{CAPTION_CENTER[1]})}}{payload}")
    return header + "\n".join(lines) + "\n"

def beat_at(beats: Sequence[Beat], t: float) -> Beat | None:
    return next((b for b in beats if b.start <= t < b.end), None)
