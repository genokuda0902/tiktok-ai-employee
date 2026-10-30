#!/usr/bin/env python3
"""cycle989: original, deterministic, narration-safe transition accents.

No external sound samples, API, credentials, or network access. Only adds a
short sound around 7 existing scene cuts; video packets are stream-copied.
Human review is mandatory; the output is never posted automatically.
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

FPS = 30
BOUNDARIES = (87, 174, 261, 348, 435, 522, 609)
SAMPLE_RATE = 48000
START_EARLY = 0.045
DURATION = 0.185


def effect_at(t: float, duration: float, seed: int = 989) -> float:
    """Original soft, airy, ascending cue; amplitude <= ~0.035."""
    if not 0 <= t < duration:
        return 0.0
    u = t / duration
    env = math.sin(math.pi * u) ** 1.6
    # Chirp 470 -> 870 Hz; smooth phase progression.
    phase = 2 * math.pi * (470 * t + (870 - 470) * t * t / (2 * duration))
    # Deterministic noise is supplied by mix_samples for a continuous texture.
    return 0.020 * env * math.sin(phase)


def mix_samples(samples: array, sample_rate: int = SAMPLE_RATE,
                boundaries=BOUNDARIES, fps: int = FPS) -> tuple[array, list[dict]]:
    if sample_rate != SAMPLE_RATE:
        raise ValueError('48 kHz PCM required')
    if fps != FPS:
        raise ValueError('30 fps scene clock required')
    out = array('h', samples)
    n = len(out)
    events = []
    for j, frame in enumerate(boundaries):
        start_s = frame / fps - START_EARLY
        start = round(start_s * sample_rate)
        length = round(DURATION * sample_rate)
        if start < 0 or start + length > n:
            raise ValueError('scene boundary outside audio')
        rng = random.Random(989 + j)
        # Local narration RMS for audit only, not for auto-gain manipulation.
        local = samples[max(0,start-2400):min(n,start+length+2400)]
        rms = math.sqrt(sum(v*v for v in local)/len(local))/32768
        max_added = 0.0
        for k in range(length):
            t = k / sample_rate
            u = t / DURATION
            env = math.sin(math.pi * u) ** 1.6
            airy = (rng.random()*2-1)*0.0065*env
            cue = effect_at(t, DURATION) + airy
            v = samples[start+k]/32768 + cue
            # Never hard-clip or compress original narration.
            if abs(v) >= 0.999:
                raise ValueError('potential clipping; lower cue gain')
            out[start+k] = max(-32768, min(32767, round(v*32768)))
            max_added = max(max_added,abs(cue))
        events.append({'frame':frame,'time_s':round(frame/fps,3),
                       'cue_start_s':round(start_s,3),'cue_duration_s':DURATION,
                       'voice_rms':round(rms,5),'max_cue_amplitude':round(max_added,5)})
    return out, events


def cmd(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def run(source: Path, target: Path, report: Path | None = None,
        boundaries=BOUNDARIES) -> dict:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle989_') as tmp:
        wav_in, wav_out = Path(tmp)/'source.wav', Path(tmp)/'cues.wav'
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-map','0:a:0','-ac','1','-ar','48000','-c:a','pcm_s16le',str(wav_in)])
        with wave.open(str(wav_in),'rb') as f:
            if f.getnchannels()!=1 or f.getframerate()!=SAMPLE_RATE or f.getsampwidth()!=2:
                raise ValueError('expected mono PCM16 48k')
            data = array('h'); data.frombytes(f.readframes(f.getnframes()))
            if sys.byteorder!='little': data.byteswap()
        mixed,events = mix_samples(data,boundaries=boundaries)
        if sys.byteorder!='little': mixed.byteswap()
        with wave.open(str(wav_out),'wb') as f:
            f.setnchannels(1);f.setsampwidth(2);f.setframerate(SAMPLE_RATE)
            f.writeframes(mixed.tobytes())
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-i',str(source),'-i',str(wav_out),'-map','0:v:0','-map','1:a:0',
             '-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000',
             '-metadata:s:a:0','language=jpn','-movflags','+faststart',str(target)])
    result={'source':str(source),'output':str(target),'audio':'AAC 48kHz mono Japanese',
            'video':'stream copy; no image or subtitle pixels altered',
            'events':events,'scene_count':len(boundaries)+1,'human_review_only':True}
    if report:
        report.parent.mkdir(parents=True,exist_ok=True)
        report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--report',type=Path)
    args=p.parse_args()
    print(json.dumps(run(args.source,args.output,args.report),ensure_ascii=False))

if __name__=='__main__': main()
