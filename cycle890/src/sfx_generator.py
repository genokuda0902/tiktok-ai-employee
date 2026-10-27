"""Deterministic, license-free UI micro-cues for review-only vertical shorts.
No external samples, paid APIs, network calls or personal data.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import random
import wave
from array import array
from pathlib import Path

SAMPLE_RATE = 48000
SCENE_CUTS = (2.88, 5.76, 8.64, 11.52, 14.40, 17.28, 20.16)
UI_TICKS = (9.45, 12.05, 18.0)

def _validate(duration: float, scene_cuts: tuple[float, ...], ui_ticks: tuple[float, ...]) -> None:
    if not (1 <= duration <= 90 and math.isfinite(duration)):
        raise ValueError('duration must be finite, between 1 and 90 seconds')
    for events in (scene_cuts, ui_ticks):
        if len(events) > 50 or any(not math.isfinite(t) or t < 0.25 or t >= duration - 0.20 for t in events):
            raise ValueError('invalid event times')
        if tuple(sorted(set(events))) != events:
            raise ValueError('events must be sorted and unique')

def make_cues(out_path: Path, duration: float = 23.033333,
              scene_cuts: tuple[float, ...] = SCENE_CUTS,
              ui_ticks: tuple[float, ...] = UI_TICKS) -> dict:
    _validate(duration, scene_cuts, ui_ticks)
    n = round(duration * SAMPLE_RATE)
    audio = array('f', [0.0]) * n
    rng = random.Random(890)
    for cut in scene_cuts:
        start = round(cut * SAMPLE_RATE)
        prev_noise = 0.0
        for i in range(min(round(0.17 * SAMPLE_RATE), n - start)):
            t = i / SAMPLE_RATE
            env = (1 - math.exp(-t / 0.009)) * math.exp(-t / 0.048)
            white = rng.uniform(-1, 1)
            prev_noise = 0.72 * prev_noise + 0.28 * white
            tone = math.sin(2 * math.pi * (660 * t + 0.5 * (480 / 0.17) * t * t))
            audio[start + i] += 0.052 * env * (0.52 * tone + 0.48 * prev_noise)
    for tick in ui_ticks:
        start = round(tick * SAMPLE_RATE)
        for i in range(min(round(0.105 * SAMPLE_RATE), n - start)):
            t = i / SAMPLE_RATE
            env = (1 - math.exp(-t / 0.002)) * math.exp(-t / 0.024)
            audio[start + i] += 0.052 * env * (0.75 * math.sin(2 * math.pi * 1046.5 * t)
                                                + 0.25 * math.sin(2 * math.pi * 1568 * t))
    peak = max(abs(x) for x in audio)
    if peak >= 0.08:
        raise RuntimeError(f'cue peak too high: {peak}')
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pcm = array('h', (int(round(max(-1, min(1, x)) * 32767)) for x in audio))
    with wave.open(str(out_path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())
    sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    return {'sample_rate': SAMPLE_RATE, 'samples': n, 'duration_seconds': n / SAMPLE_RATE,
            'scene_cuts': list(scene_cuts), 'ui_ticks': list(ui_ticks),
            'cue_peak_dbfs': round(20 * math.log10(peak), 2) if peak else None,
            'sha256': sha, 'source': 'pure-python mathematical synthesis; no third-party assets'}

def parse_times(s: str) -> tuple[float, ...]:
    return tuple(float(x) for x in s.split(',') if x.strip())

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--duration', type=float, default=23.033333)
    p.add_argument('--cuts', type=parse_times, default=SCENE_CUTS)
    p.add_argument('--clicks', type=parse_times, default=UI_TICKS)
    args = p.parse_args()
    print(json.dumps(make_cues(args.out, args.duration, args.cuts, args.clicks), ensure_ascii=False, indent=2))
