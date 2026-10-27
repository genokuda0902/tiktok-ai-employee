"""Offline narration-first mixing for 10-genre image-slide videos.

Uses only Python stdlib. Cues are ducked while the *reference voice* is active.
This is an acoustic priority check, NOT Japanese speech recognition or semantic QA.
No paid API, upload, auto-post or third-party audio sample.
"""
from __future__ import annotations
import argparse
from array import array
import json
import math
import wave
from pathlib import Path

RATE = 48000
HOP = 480                         # 10 ms
VOICE_THRESHOLD = 0.025           # RMS, full scale
DUCK_GAIN = 0.25                  # -12.04 dB for speech-active frames
VOICE_GAIN = 0.94


def read_mono_pcm16(path: Path) -> array:
    with wave.open(str(path), 'rb') as f:
        if (f.getnchannels(), f.getsampwidth(), f.getframerate(), f.getcomptype()) != (1, 2, RATE, 'NONE'):
            raise ValueError('expected mono PCM16 48 kHz WAV')
        out = array('h')
        out.frombytes(f.readframes(f.getnframes()))
    return out


def gain_envelope(voice: array, cue: array, threshold=VOICE_THRESHOLD, min_gain=DUCK_GAIN):
    if not (0 < threshold < 1 and 0 < min_gain <= 1):
        raise ValueError('invalid threshold or min gain')
    if abs(len(voice) - len(cue)) > RATE // 10:
        raise ValueError('audio duration mismatch >100ms')
    n = min(len(voice), len(cue))
    if n < RATE:
        raise ValueError('audio must be at least 1 second')
    # Activity is detected on 20ms windows, updated every 10ms.
    rms = []
    for i in range(0, n, HOP):
        lo = max(0, i - HOP)
        hi = min(n, i + HOP)
        rms.append(math.sqrt(sum(x*x for x in voice[lo:hi]) / max(1, hi-lo)) / 32768)
    # 10ms attack / 90ms release. Continuous envelope avoids zipper clicks.
    gains = []
    g = 1.0
    for level in rms:
        target = min_gain if level >= threshold else 1.0
        tau = 0.010 if target < g else 0.090
        alpha = 1 - math.exp(-0.010 / tau)
        g += alpha * (target - g)
        gains.append(g)
    return gains, rms


def mix(voice_file: Path, cue_file: Path, out_file: Path) -> dict:
    voice = read_mono_pcm16(voice_file)
    cue = read_mono_pcm16(cue_file)
    if len(voice) < len(cue):
        voice.extend([0] * (len(cue) - len(voice)))
    gains, rms = gain_envelope(voice, cue)
    n = len(cue)
    out = array('h')
    baseline_overlap = 0.0
    ducked_overlap = 0.0
    active_cue_samples = 0
    speech_cue_samples = 0
    quiet_cue_samples = 0
    quiet_gain_sum = 0.0
    peak = 0
    for i in range(n):
        frame = min(i // HOP, len(gains)-1)
        # Linear interpolation removes frame-edge gain discontinuities.
        nxt = min(frame + 1, len(gains)-1)
        frac = (i % HOP) / HOP
        g = gains[frame] * (1-frac) + gains[nxt] * frac
        v = voice[i] / 32768
        c = cue[i] / 32768
        sample = VOICE_GAIN * v + c * g
        if abs(sample) >= 0.99:
            raise RuntimeError('clipping risk')
        q = int(round(sample * 32767))
        out.append(q)
        peak = max(peak, abs(q))
        if abs(c) > 0.0001:
            active_cue_samples += 1
            if rms[frame] >= VOICE_THRESHOLD:
                speech_cue_samples += 1
                baseline_overlap += c*c
                ducked_overlap += (c*g)**2
            else:
                quiet_cue_samples += 1
                quiet_gain_sum += g
    out_file = Path(out_file)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_file), 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(out.tobytes())
    reduction_db = 10 * math.log10(ducked_overlap / baseline_overlap) if baseline_overlap > 0 else None
    return {
        'sample_rate': RATE, 'samples': n, 'seconds': n/RATE,
        'voice_threshold_rms': VOICE_THRESHOLD, 'minimum_cue_gain': DUCK_GAIN,
        'speech_overlap_cue_samples': speech_cue_samples,
        'quiet_cue_samples': quiet_cue_samples,
        'speech_overlap_cue_energy_reduction_db': round(reduction_db, 2) if reduction_db is not None else None,
        'quiet_cue_mean_gain': round(quiet_gain_sum / quiet_cue_samples, 3) if quiet_cue_samples else None,
        'output_peak_dbfs': round(20*math.log10(peak/32768), 2) if peak else None,
        'purpose': 'voice-priority acoustic mixing; no semantic ASR performed',
        'status': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('voice', type=Path)
    p.add_argument('cues', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--metrics', type=Path)
    args = p.parse_args()
    result = mix(args.voice, args.cues, args.output)
    if args.metrics:
        args.metrics.parent.mkdir(parents=True, exist_ok=True)
        args.metrics.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
