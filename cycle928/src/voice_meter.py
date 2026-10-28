#!/usr/bin/env python3
"""Cycle928: audio-reactive header meter; visual indicator only, not ASR or approval."""
from __future__ import annotations
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

FPS = 30
FRAMES = 691
SIZE = (1080, 1920)
METER_XY = (468, 55)
METER_SIZE = (260, 64)
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
GENRE_COLORS = {
    'ai_work': '#2ED7C5', 'finance': '#6BC7FF', 'health': '#8BDFB1',
    'travel': '#A0B9FF', 'beauty': '#F0B5E3', 'cooking': '#FFBD87',
    'education': '#C9B4FF', 'career': '#F2D18E',
    'lifestyle': '#E9B0C9', 'technology': '#8DDDE6',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()

def audio_rms(source):
    """Decode existing audio as 16 kHz mono signed PCM; no internet, no new voice."""
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(source),
           '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', 'pipe:1']
    data = subprocess.check_output(cmd, timeout=90)
    pcm = array('h')
    pcm.frombytes(data)
    values = []
    for frame in range(FRAMES):
        start = round(frame * 16000 / FPS)
        end = round((frame + 1) * 16000 / FPS)
        window = pcm[start:end]
        if not window:
            values.append(0.0)
        else:
            values.append(math.sqrt(sum(v * v for v in window) / len(window)) / 32768)
    return values

def envelope(rms):
    """Amplitude envelope, fast attack / slow release; silence remains low."""
    levels, prior = [], 0.0
    for value in rms:
        db = 20 * math.log10(max(value, 1e-7))
        target = max(0.0, min(1.0, (db + 48) / 34))
        alpha = 0.57 if target > prior else 0.22
        prior += alpha * (target - prior)
        levels.append(prior)
    return levels

def make_meter(level, frame, genre='ai_work'):
    if genre not in GENRE_COLORS:
        raise ValueError('unsupported genre')
    if not 0 <= level <= 1:
        raise ValueError('level must be in [0,1]')
    im = Image.new('RGBA', METER_SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1, 1, 258, 62), radius=21, fill=(12, 41, 67, 255), outline=(56, 112, 140, 255), width=2)
    f = ImageFont.truetype(FONT, 21) if Path(FONT).exists() else ImageFont.load_default()
    d.text((14, 16), 'VOICE', font=f, fill=(192, 231, 240, 255))
    c = tuple(bytes.fromhex(GENRE_COLORS[genre][1:]))
    for i in range(8):
        weight = 0.58 + 0.42 * (0.5 + 0.5 * math.sin(i * 1.65 + frame * 0.19))
        height = round(6 + 38 * level * weight)
        x = 103 + 17 * i
        d.rounded_rectangle((x, 53 - height, x + 9, 53), radius=4, fill=(*c, 255))
    return im

def render(source, output, genre='ai_work', expected_sha=None):
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    if genre not in GENRE_COLORS:
        raise ValueError('unsupported genre')
    if expected_sha and sha256(source) != expected_sha:
        raise RuntimeError('SOURCE_SHA_MISMATCH')
    output.parent.mkdir(parents=True, exist_ok=True)
    rms = audio_rms(source)
    levels = envelope(rms)
    with tempfile.TemporaryDirectory(prefix='cycle928_meter_') as td:
        root = Path(td)
        for frame, level in enumerate(levels):
            make_meter(level, frame, genre).save(root / f'meter_{frame:04d}.png')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
               '-i', str(source), '-framerate', str(FPS), '-i', str(root / 'meter_%04d.png'),
               '-filter_complex', f'[0:v][1:v]overlay={METER_XY[0]}:{METER_XY[1]}:shortest=1:format=auto[v]',
               '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast',
               '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-frames:v', str(FRAMES),
               '-movflags', '+faststart', str(output)]
        subprocess.run(cmd, check=True, timeout=240)
    return {
        'cycle': 928, 'source_sha256': sha256(source), 'output_sha256': sha256(output),
        'audio_rms_min_max': [min(rms), max(rms)],
        'meter_envelope_min_max': [min(levels), max(levels)],
        'silent_frames_rms_below_0_01': sum(x < 0.01 for x in rms),
        'active_frames_rms_above_0_08': sum(x > 0.08 for x in rms),
        'frame_count': FRAMES, 'genre': genre, 'policy': POLICY,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--genre', choices=list(GENRE_COLORS), default='ai_work')
    p.add_argument('--expected-source-sha')
    p.add_argument('--report')
    a = p.parse_args()
    report = render(a.source, a.output, a.genre, a.expected_source_sha)
    if a.report:
        Path(a.report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))

if __name__ == '__main__':
    main()
