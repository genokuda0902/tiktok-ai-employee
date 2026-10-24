"""Cycle816 reusable audio-pause-aware Japanese caption timing.
No API calls, no publishing, no automatic merges.
This is a pause-based estimate, NOT word-level forced alignment.
"""
from __future__ import annotations
import re
import subprocess

GENRE_ACCENTS = {
    "ai_work": "#77d5ff", "beauty": "#ffa2c3",
    "love_psychology": "#c3a0ff", "money_saving": "#ffd475",
    "sales_business": "#61f0c7", "career": "#84b9ff",
    "health_life": "#b4e97d", "science": "#86d9ff",
    "travel_food": "#ffbb8b", "product_life": "#d7b0ff",
}
PHRASES = [
    ["仕事ができる人は、", "質問が", "違う。"],
    ["まず、", "目指すゴールを", "確認する。"],
    ["次に、", "今の数字を", "確かめる。"],
    ["そして、", "理想との差を", "一つに絞る。"],
    ["原因には、", "なぜを", "三回重ねる。"],
    ["対策は、", "今日できる", "行動に変える。"],
    ["結果を見て、", "また", "修正する。"],
    ["小さな改善が、", "強いチームを", "つくる。"],
]

def detect_silences(source, duration, noise_db=-34, minimum_pause=0.16):
    """Return [start, end] seconds using local FFmpeg's silencedetect."""
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(source),
           "-af", f"silencedetect=noise={noise_db}dB:d={minimum_pause}",
           "-f", "null", "-"]
    run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, check=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", run.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", run.stderr)]
    return [(max(0, s), min(duration, ends[i] if i < len(ends) else duration))
            for i, s in enumerate(starts)]

def voiced_runs(start, end, silences):
    runs, cursor = [], start
    for a, b in silences:
        if b <= start or a >= end:
            continue
        a, b = max(start, a), min(end, b)
        if a > cursor + 0.07:
            runs.append((cursor, a))
        cursor = max(cursor, b)
    if cursor < end - 0.07:
        runs.append((cursor, end))
    return runs

def voice_guided_cuts(start, end, silences):
    """3 phrase spans with speech-onset gating and silence-informed cuts."""
    runs = voiced_runs(start, end, silences)
    if not runs:
        return [start, start+(end-start)/3, start+2*(end-start)/3, end], False
    onset = max(start, runs[0][0])
    offset = min(end, runs[-1][1]+0.16)
    gaps = [(runs[i][1]+runs[i+1][0])/2 for i in range(len(runs)-1)]
    if len(gaps) >= 2:
        first, second = gaps[:2]
    elif len(gaps) == 1:
        first = gaps[0]
        second = first + (offset-first)*0.5
    else:
        first = onset + (offset-onset)*0.34
        second = onset + (offset-onset)*0.68
    first = max(onset+0.12, min(first, offset-0.24))
    second = max(first+0.12, min(second, offset-0.12))
    return [onset, first, second, offset], True
