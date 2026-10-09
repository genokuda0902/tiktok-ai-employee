"""Allocate frame-accurate Japanese subtitle dwell time for review videos."""
from dataclasses import dataclass
from math import ceil
from unicodedata import east_asian_width, category

@dataclass(frozen=True)
class Beat:
    text: str
    start: int
    end: int

def visual_units(text):
    if not isinstance(text, str) or not text.strip() or '\n' in text:
        raise ValueError("Invalid subtitle")
    return sum(1.0 if east_asian_width(c) in "FW"
               else 0.4 if category(c).startswith("P")
               else 0.62 for c in text)

def allocate(caption_pairs, fps=30, frames_per_scene=75, limit=13.5):
    if not caption_pairs or fps <= 0 or frames_per_scene < 48 or limit <= 0:
        raise ValueError("Invalid timing")
    beats = []
    for index, pair in enumerate(caption_pairs):
        if len(pair) != 2:
            raise ValueError("Exactly two subtitles per scene")
        a, b = pair
        ua, ub = visual_units(a), visual_units(b)
        if (ua + ub) * fps / frames_per_scene > limit:
            raise ValueError("Insufficient reading time")
        lo = max(24, ceil(ua * fps / limit))
        hi = frames_per_scene - max(24, ceil(ub * fps / limit))
        if lo > hi:
            raise ValueError("Insufficient frame budget")
        cut = min(hi, max(lo, round(frames_per_scene * ua / (ua + ub))))
        start = index * frames_per_scene
        beats += [Beat(a, start, start + cut),
                  Beat(b, start + cut, start + frames_per_scene)]
    return beats

def max_rate(beats, fps=30):
    return max(visual_units(b.text) * fps / (b.end - b.start) for b in beats)
