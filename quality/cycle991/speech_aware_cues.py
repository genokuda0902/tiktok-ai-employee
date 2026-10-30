#!/usr/bin/env python3
"""Cycle991: speech-aware original transition cues. Free, offline, review-only.

Input is the PRE-cue source video (cycle987), not cycle989: avoids double cues.
Video packets are copied; burned-in captions and visual frames are unchanged.
"""
from __future__ import annotations
import argparse
from array import array
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import wave

RATE = 48000
FPS = 30
DEFAULT_FRAMES = (87, 174, 261, 348, 435, 522, 609)
DURATION = 0.185
EARLY = 0.045

def gain_for_voice(rms: float) -> float:
    """Reduce cue strength when speech is present, never amplify above 0.85."""
    return max(0.18, min(0.85, 0.045 / (rms + 0.010)))

def cue_sample(t: float, index: int, noise: float) -> float:
    if not 0 <= t < DURATION:
        return 0.0
    envelope = math.sin(math.pi * t / DURATION) ** 1.6
    phase = 2 * math.pi * (470 * t + 400 * t * t / (2 * DURATION))
    return envelope * (0.020 * math.sin(phase) + 0.0065 * noise)

def process(samples: array, boundaries=DEFAULT_FRAMES) -> tuple[array, list[dict]]:
    output = array('h', samples)
    report = []
    n = len(samples)
    for j, frame in enumerate(boundaries):
        start = round((frame / FPS - EARLY) * RATE)
        length = round(DURATION * RATE)
        if start < 0 or start + length > n:
            raise ValueError('boundary outside source audio')
        lo, hi = max(0, start - round(.12 * RATE)), min(n, start + round(.24 * RATE))
        rms = math.sqrt(sum((v / 32768.0) ** 2 for v in samples[lo:hi]) / (hi-lo))
        gain = gain_for_voice(rms)
        rng = random.Random(989 + j)
        for k in range(length):
            t = k / RATE
            cue = cue_sample(t, j, rng.random()*2 - 1) * gain
            value = samples[start+k]/32768 + cue
            if abs(value) >= .99:
                raise ValueError('audio would clip')
            output[start+k] = round(value * 32768)
        report.append({'frame': frame, 'time_s': round(frame/FPS, 3),
                       'speech_context_rms': round(rms, 6),
                       'adaptive_gain': round(gain, 4),
                       'original_cue_gain': 1.0})
    return output, report

def run(source: Path, target: Path, report_path: Path | None = None,
        boundaries=DEFAULT_FRAMES) -> dict:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle991_') as tmp:
        inp, out = Path(tmp)/'in.wav', Path(tmp)/'out.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-vn',
                        '-ac','1','-ar',str(RATE),'-c:a','pcm_s16le',str(inp)],check=True)
        with wave.open(str(inp),'rb') as f:
            if (f.getnchannels(), f.getframerate(), f.getsampwidth()) != (1,RATE,2):
                raise ValueError('expected mono 48kHz 16-bit PCM')
            samples = array('h'); samples.frombytes(f.readframes(f.getnframes()))
            if sys.byteorder != 'little': samples.byteswap()
        mixed, cues = process(samples, boundaries)
        if sys.byteorder != 'little': mixed.byteswap()
        with wave.open(str(out),'wb') as f:
            f.setnchannels(1); f.setframerate(RATE); f.setsampwidth(2)
            f.writeframes(mixed.tobytes())
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-i',str(out),
                        '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac',
                        '-b:a','192k','-ar',str(RATE),'-metadata:s:a:0','language=jpn',
                        '-movflags','+faststart',str(target)],check=True)
    report = {'cycle':991,'source':str(source),'output':str(target),
              'improvement':'speech-aware attenuation of original transition sounds',
              'cues':cues,'no_upload':True,'human_review_required':True}
    if report_path:
        report_path.parent.mkdir(parents=True,exist_ok=True)
        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument('source',type=Path);p.add_argument('target',type=Path)
    p.add_argument('--report',type=Path)
    p.add_argument('--boundaries',default=','.join(map(str,DEFAULT_FRAMES)))
    a=p.parse_args()
    frames=tuple(int(v) for v in a.boundaries.split(',') if v)
    print(json.dumps(run(a.source,a.target,a.report,frames),ensure_ascii=False))

if __name__=='__main__': main()
