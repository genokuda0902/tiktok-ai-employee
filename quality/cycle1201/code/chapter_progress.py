#!/usr/bin/env python3
"""Offline scene-aware progress rail for portrait Japanese-captioned slide videos.

Adds a discreet progress rail in a top safe-area. No OCR, cloud, personal
information, stock media, or posting. H.264 re-encoded; AAC stream-copied.
Scene starts are explicit editorial metadata, never guessed from narration.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

FPS = 30
GENRE_ACCENTS = {
    'ai': '45d7c8', 'business': '84b9f0', 'money': '60d6ac',
    'learning': 'a5bfff', 'health': '68dcb5', 'food': '9bdc8a',
    'travel': '73cce9', 'beauty': 'c7a6ed', 'career': '80bdf2',
    'life': '91d8bb',
}
DEFAULT_SCENE_STARTS = (42, 96, 171, 252, 333, 414, 501, 579)


def probe(path):
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                        '-of', 'json', str(path)], check=True, text=True, capture_output=True)
    return json.loads(p.stdout)


def validate_source(info):
    v = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
    a = next((s for s in info['streams'] if s['codec_type'] == 'audio'), None)
    if not v or not a:
        raise ValueError('Video and audio streams required')
    if (int(v['width']), int(v['height']), v['r_frame_rate']) != (1080, 1920, '30/1'):
        raise ValueError('Input must be exactly 1080x1920 at 30fps')
    if a['codec_name'] != 'aac':
        raise ValueError('Input must contain AAC narration for bitstream copy')
    return int(v.get('nb_frames') or round(float(info['format']['duration']) * FPS))


def validate_scene_starts(starts, frames):
    if not 4 <= len(starts) <= 16:
        raise ValueError('4–16 scenes supported')
    if any(not isinstance(n, int) for n in starts):
        raise ValueError('Scene starts must be integer frame indices')
    if starts[0] < 0 or starts[-1] >= frames or list(starts) != sorted(set(starts)):
        raise ValueError('Scene starts must be unique, increasing and within video')
    return tuple(starts)


def segment_geometry(n, left=78, right=854, gap=10, y=155, height=7):
    if n < 4 or n > 16: raise ValueError('Invalid scene count')
    if not (0 <= left < right <= 930 and 128 <= y <= 175 and 4 <= height <= 12):
        raise ValueError('Progress rail must stay in top safe area')
    width = (right - left - gap * (n - 1)) // n
    if width < 20: raise ValueError('Progress segments too narrow')
    return [(left + i * (width + gap), y, width, height) for i in range(n)]


def filter_graph(starts, frames, accent='45d7c8'):
    starts = validate_scene_starts(starts, frames)
    if accent not in GENRE_ACCENTS.values():
        raise ValueError('Use an approved 10-genre accent color')
    parts = []
    geometry = segment_geometry(len(starts))
    # Dark inactive track, colored completed steps, bright current step.
    for x, y, w, h in geometry:
        parts.append(f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0x28515b@0.78:t=fill')
    for i, (x, y, w, h) in enumerate(geometry):
        start = starts[i]
        stop = starts[i + 1] - 1 if i + 1 < len(starts) else frames - 1
        if i + 1 < len(starts):
            parts.append(f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0x{accent}@0.76:'
                         f't=fill:enable=gte(n\\,{starts[i + 1]})')
        parts.append(f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0xdafaf5@0.98:'
                     f't=fill:enable=between(n\\,{start}\\,{stop})')
    return ','.join(parts)


def render(src, dst, starts=DEFAULT_SCENE_STARTS, genre='ai', crf=17, limit_frames=None):
    if genre not in GENRE_ACCENTS: raise ValueError('Unknown genre')
    frames = validate_source(probe(src))
    if limit_frames is not None: frames = min(frames, int(limit_frames))
    starts = validate_scene_starts(starts, frames)
    if not (14 <= crf <= 23): raise ValueError('CRF must be between 14 and 23')
    graph = filter_graph(starts, frames, GENRE_ACCENTS[genre])
    dst = Path(dst); dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(src),
           '-vf', graph, '-map', '0:v:0', '-map', '0:a:0',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf),
           '-pix_fmt', 'yuv420p', '-r', '30', '-fps_mode', 'cfr',
           '-c:a', 'copy', '-frames:v', str(frames), '-movflags', '+faststart',
           '-metadata:s:a:0', 'language=jpn', str(dst)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError('ffmpeg render failed: ' + p.stderr[-2000:])
    return {'genre': genre, 'frames_expected': frames, 'scene_starts': list(starts),
            'output': str(dst), 'rail_geometry': segment_geometry(len(starts))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source'); ap.add_argument('output')
    ap.add_argument('--genre', choices=list(GENRE_ACCENTS), default='ai')
    ap.add_argument('--starts', default=','.join(map(str, DEFAULT_SCENE_STARTS)),
                    help='Comma-separated scene start frame indices')
    ap.add_argument('--crf', type=int, default=17)
    a = ap.parse_args()
    starts = tuple(int(v) for v in a.starts.split(','))
    print(json.dumps(render(a.source, a.output, starts, a.genre, a.crf), ensure_ascii=False))

if __name__ == '__main__':
    main()
