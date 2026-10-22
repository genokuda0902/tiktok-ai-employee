"""Offline audio-reactive subtitle core. Zero paid services, no posting."""
from __future__ import annotations
import math
import re

FPS = 30
WIDTH, HEIGHT = 1080, 1920
PANEL = (54, 1366, 708, 190)

def rms_windows(samples, sample_rate, fps=FPS):
    if sample_rate <= 0 or fps <= 0:
        raise ValueError("sample_rate and fps must be positive")
    count = math.ceil(len(samples) * fps / sample_rate)
    result = []
    for i in range(count):
        lo = round(i * sample_rate / fps)
        hi = min(len(samples), round((i + 1) * sample_rate / fps))
        part = samples[lo:hi]
        result.append(math.sqrt(sum(float(x)*float(x) for x in part)/len(part)) if part else 0.0)
    return result

def smooth_envelope(rms, floor=.008, scale=.11):
    if scale <= 0:
        raise ValueError("scale must be positive")
    output = []
    previous = 0.0
    for sample in rms:
        level = max(0.0, min(1.0, (float(sample)-floor)/scale))
        inertia = .30 if level > previous else .72
        previous = previous*inertia + level*(1-inertia)
        output.append(previous)
    return output

def waveform_bars(level, count=12):
    if count <= 0:
        raise ValueError("count must be positive")
    strength = max(0.0, min(1.0, level))
    return [round(5+31*strength*(.55+.45*abs(math.sin(i*1.35+.65)))) for i in range(count)]

def cue_progress(frame_time, start, end):
    if end <= start:
        raise ValueError("cue end must follow start")
    return max(0.0, min(1.0, (frame_time-start)/(end-start)))

def panel_within_safe_area(width=WIDTH, height=HEIGHT):
    x,y,w,h = PANEL
    return x+w < width-180 and y+h < height-300

def parse_accent(value):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}",value):
        raise ValueError("Expected #RRGGBB")
    return tuple(int(value[i:i+2],16) for i in (1,3,5))
