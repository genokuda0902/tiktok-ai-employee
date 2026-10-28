#!/usr/bin/env python3
"""Original, speech-aware scene-change sound design for review-only vertical videos.

No downloaded samples, third-party TTS, uploads, posting, or paid APIs.
Source video is stream-copied, while AAC audio is re-encoded after mixing.
Speech-aware means RMS-based ducking, NOT ASR or semantic alignment.
"""
from __future__ import annotations
import argparse
import array
import hashlib
import json
import math
import random
import struct
import subprocess
import sys
import wave
from pathlib import Path

SAMPLE_RATE = 48000
FPS = 30
FRAME_COUNT = 691
SCENE_START_FRAMES = (87, 174, 261, 348, 435, 522, 609)
DURATION = FRAME_COUNT / FPS
CUE_SECONDS = 0.22
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
# A consistent sonic identity with 10 deterministic, restrained pitch variants.
GENRE_PITCH = {
    'ai_work': 1.00, 'finance': 0.96, 'health': 1.04,
    'travel': 1.08, 'beauty': 1.06, 'cooking': 0.92,
    'education': 1.02, 'career': 0.98, 'lifestyle': 1.03,
    'technology': 1.10,
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def run(cmd, timeout=180):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=timeout)

def decode_mono_float(path):
    p = subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(path),
        '-map', '0:a:0', '-vn', '-ar', str(SAMPLE_RATE), '-ac', '1',
        '-f', 'f32le', 'pipe:1'
    ], check=True, capture_output=True, timeout=120)
    raw = p.stdout
    if len(raw) % 4:
        raise RuntimeError('INVALID_AUDIO_BYTES')
    samples = array.array('f')
    samples.frombytes(raw)
    if sys.byteorder != 'little':
        samples.byteswap()
    return samples

def rms(samples, start, end):
    a = max(0, int(start * SAMPLE_RATE))
    b = min(len(samples), int(end * SAMPLE_RATE))
    if b <= a:
        return 0.0
    return math.sqrt(sum(float(v) * v for v in samples[a:b]) / (b - a))

def cue_gain(voice_rms, threshold=0.027):
    """Less SFX when the voice is already loud; no speech content inference."""
    return 0.022 if voice_rms >= threshold else 0.038

def synthesize_sfx(voice_samples, genre='ai_work', seed=931):
    if genre not in GENRE_PITCH:
        raise ValueError('unsupported genre')
    n = round(DURATION * SAMPLE_RATE)
    track = array.array('f', [0.0]) * n
    info = []
    pitch = GENRE_PITCH[genre]
    for index, frame in enumerate(SCENE_START_FRAMES, 1):
        cut = frame / FPS
        # Window covers the cut, not the entire narration. It does not infer words.
        voice_level = rms(voice_samples, cut - 0.12, cut + 0.12)
        gain = cue_gain(voice_level)
        rng = random.Random(seed + index * 97)
        filtered = 0.0
        start = int((cut - 0.035) * SAMPLE_RATE)
        count = int(CUE_SECONDS * SAMPLE_RATE)
        for j in range(count):
            t = j / SAMPLE_RATE
            x = t / CUE_SECONDS
            # Smooth attack/release: no click; fast transient with a soft air tail.
            envelope = math.sin(math.pi * x) ** 2 * math.exp(-0.8 * x)
            white = 2.0 * rng.random() - 1.0
            filtered = 0.86 * filtered + 0.14 * white
            chirp = math.sin(2.0 * math.pi * (850.0 * pitch * t - 450.0 * t * t))
            sample = gain * envelope * (0.78 * filtered + 0.22 * chirp)
            pos = start + j
            if 0 <= pos < n:
                track[pos] += sample
        info.append({
            'transition': index, 'frame': frame, 'time_s': round(cut, 3),
            'voice_rms_dbfs': round(20 * math.log10(max(voice_level, 1e-8)), 2),
            'sfx_gain': gain,
        })
    return track, info

def write_wav(path, track):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        # Keep under clipping. Source voice is never baked into this reusable stem.
        f.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, x)) * 32767)) for x in track))

def render(source, output, sfx_path, genre='ai_work', expected_source_sha=None):
    source, output, sfx_path = Path(source), Path(output), Path(sfx_path)
    if not source.is_file():
        raise FileNotFoundError(source)
    if genre not in GENRE_PITCH:
        raise ValueError('unsupported genre')
    src_hash = sha256(source)
    if expected_source_sha and expected_source_sha != src_hash:
        raise RuntimeError('SOURCE_SHA_MISMATCH')
    voice = decode_mono_float(source)
    sfx, cues = synthesize_sfx(voice, genre)
    write_wav(sfx_path, sfx)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
        '-i', str(source), '-i', str(sfx_path),
        '-filter_complex', '[0:a:0]aresample=48000,asetpts=PTS-STARTPTS[voice];'
                           '[1:a:0]aresample=48000,asetpts=PTS-STARTPTS[sfx];'
                           '[voice][sfx]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]',
        '-map', '0:v:0', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-ar', str(SAMPLE_RATE), '-ac', '1', '-t', f'{DURATION:.6f}',
        '-movflags', '+faststart', str(output)
    ]
    run(cmd, timeout=180)
    return {
        'cycle': 931, 'genre': genre, 'source_sha256': src_hash,
        'output_sha256': sha256(output), 'sfx_sha256': sha256(sfx_path),
        'source_audio': 'inherited Japanese narration; NOT independently transcribed',
        'visuals': 'video bitstream copied; burned-in Japanese captions untouched',
        'new_feature': '7 original deterministic speech-RMS-ducked scene-change sound cues',
        'cues': cues, 'policy': POLICY,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--sfx-wav', required=True)
    p.add_argument('--genre', choices=list(GENRE_PITCH), default='ai_work')
    p.add_argument('--expected-source-sha')
    p.add_argument('--report')
    args = p.parse_args()
    report = render(args.source, args.output, args.sfx_wav, args.genre, args.expected_source_sha)
    if args.report:
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
