#!/usr/bin/env python3
"""10-genre reusable, strictly localized caption legibility pass.

Input is a consented, locally available vertical video. This never creates narration,
changes wording, accesses personal information or posts anything.
"""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

DEFAULT_ROI = (100, 1420, 720, 180)
GENRES = ('ai', 'business', 'money', 'learning', 'health',
          'food', 'travel', 'beauty', 'career', 'life')
# Shared visual grammar: all ten genre presets use the same subtitle safe-zone.
GENRE_ROI = {name: DEFAULT_ROI for name in GENRES}

def filter_graph(width: int = 1080, height: int = 1920,
                 roi: tuple[int, int, int, int] = DEFAULT_ROI,
                 strength: float = 0.45) -> str:
    x, y, w, h = roi
    if width <= 0 or height <= 0 or min(x, y) < 0 or min(w, h) <= 0:
        raise ValueError('invalid dimensions')
    if x + w > width or y + h > height:
        raise ValueError('caption ROI outside frame')
    if x % 2 or y % 2 or w % 2 or h % 2:
        raise ValueError('ROI must be chroma-aligned (even values)')
    if not 0 <= strength <= 1.5:
        raise ValueError('strength outside conservative range')
    return (f'[0:v]split=2[base][cropin];'
            f'[cropin]crop={w}:{h}:{x}:{y},unsharp=5:5:{strength}:5:5:0[caption];'
            f'[base][caption]overlay={x}:{y}:shortest=1,format=yuv420p[v]')

def run(input_path: Path, output_path: Path, *, strength: float = 0.45) -> None:
    if input_path.resolve() == output_path.resolve():
        raise ValueError('refuse to overwrite source')
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    graph = filter_graph(strength=strength)
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-y', '-loglevel', 'error',
           '-i', str(input_path), '-filter_complex', graph,
           '-map', '[v]', '-map', '0:a?', '-map_metadata', '0', '-map_chapters', '0',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
           '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart',
           str(output_path)]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('input', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--strength', type=float, default=0.45)
    a = p.parse_args()
    run(a.input, a.output, strength=a.strength)
