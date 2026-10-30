#!/usr/bin/env python3
"""Replace overlapping/cropped slide headlines with one safe, stable Japanese title.

Cycle1031: intentionally preserves audio, burned captions, metadata and chapters.
This does NOT verify speech/subtitle semantics or grant publication approval.
Requires FFmpeg drawtext and a locally installed CJK font; no paid services.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import subprocess

GENRE_ACCENTS = {
    'ai_work': '0x39DDC6', 'trivia': '0xF0C76B', 'cooking': '0xF9A96C',
    'beauty': '0xF6B3C9', 'money': '0x7DDB99', 'health': '0x73D5B4',
    'travel': '0x75C9F2', 'product': '0xA4BBFF', 'story': '0xD8A9F2',
    'work_skills': '0x6CD8D6',
}
# First scene's headline was already rebuilt in cycle1023: do not cover it.
# Explicit chapter-aligned intervals avoid cutting the preceding/following scene.
DEFAULT_SCENES = [
    (2.633, 5.800, '繰り返す作業を書き出す'),
    (5.800, 8.600, '完成形の見本を用意'),
    (8.600, 11.333, '目的と条件を具体的に'),
    (11.333, 14.100, 'AIの出力を自分で確認'),
    (14.100, 16.767, '修正点は一つずつ伝える'),
    (16.767, 19.767, '使える指示を保存する'),
    (19.767, 22.500, '小さな時短を習慣に'),
]
# Coordinates valid only for 1080x1920 with original caption box at y~1180-1390.
HEADER_RECT = (32, 154, 1016, 300)
CAPTION_MIN_Y = 1150

def validate_scenes(scenes, width=1080, height=1920):
    if (width, height) != (1080, 1920):
        raise ValueError('Expected 1080x1920 template; refusing unsafe overlay')
    x, y, w, h = HEADER_RECT
    if x < 0 or y < 145 or x + w > width or y + h >= CAPTION_MIN_Y:
        raise ValueError('Header overlaps protected regions')
    if not scenes or len(scenes) > 10:
        raise ValueError('Expected 1..10 chapters')
    prev_end = 0
    for start, end, title in scenes:
        if not (0 <= start < end <= 60) or start < prev_end - 1e-4:
            raise ValueError('Invalid or overlapping chapter intervals')
        if not title or len(title) > 20 or '\n' in title or ':' in title or "'" in title:
            raise ValueError('Title must be short, single-line Japanese safe text')
        prev_end = end
    return scenes

def find_cjk_font():
    candidates = [
        os.environ.get('TIKTOK_CJK_FONT', ''),
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/arphic/ukai.ttc',
    ]
    for path in candidates:
        if path and Path(path).is_file():
            return path
    try:
        font = subprocess.check_output(['fc-match', '-f', '%{file}', 'sans:lang=ja'], text=True).strip()
        if Path(font).is_file():
            return font
    except (OSError, subprocess.CalledProcessError):
        pass
    raise FileNotFoundError('No Japanese CJK font installed; install fonts-noto-cjk')

def filtergraph(genre='ai_work', scenes=DEFAULT_SCENES, fontfile=None):
    validate_scenes(scenes)
    if genre not in GENRE_ACCENTS:
        raise ValueError('Unknown genre')
    fontfile = fontfile or find_cjk_font()
    if not Path(fontfile).is_file():
        raise FileNotFoundError(fontfile)
    accent = GENRE_ACCENTS[genre]
    enable = '+'.join(f'between(t,{s:.3f},{e-0.001:.3f})' for s,e,_ in scenes)
    f = [
        f"drawbox=x=32:y=154:w=1016:h=300:color=0x07182B@1:t=fill:enable='{enable}'",
        f"drawbox=x=32:y=154:w=1016:h=300:color={accent}@0.88:t=3:enable='{enable}'",
        f"drawbox=x=60:y=190:w=8:h=210:color={accent}@1:t=fill:enable='{enable}'",
    ]
    font = fontfile.replace('\\', '\\\\').replace(':', '\\:').replace("'", "\\'")
    for i, (start, end, title) in enumerate(scenes, 2):
        e = f'gte(t,{start:.3f})*lt(t,{end:.3f})'
        f.append(f"drawtext=fontfile='{font}':text='KEY IDEA  /  {i:02d}  /  08':fontcolor={accent}:fontsize=28:x=95:y=186:enable='{e}'")
        f.append(f"drawtext=fontfile='{font}':text='{title}':fontcolor=white:fontsize=54:x=95:y=258:enable='{e}'")
        f.append(f"drawtext=fontfile='{font}':text='AI WORKFLOW  /  HUMAN REVIEW':fontcolor=0xB4C8D7:fontsize=23:x=95:y=352:enable='{e}'")
    f.append('format=yuv420p')
    return ','.join(f)

def render(src, dst, genre='ai_work', scenes=DEFAULT_SCENES, fontfile=None, preset='veryfast', crf=19):
    if not Path(src).is_file():
        raise FileNotFoundError(src)
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    graph = filtergraph(genre, scenes, fontfile)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(src),
           '-vf', graph, '-map', '0:v:0', '-map', '0:a:0', '-map', '0:d?',
           '-map_metadata', '0', '-map_chapters', '0',
           '-c:v', 'libx264', '-preset', preset, '-crf', str(crf),
           '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-c:d', 'copy',
           '-movflags', '+faststart', str(dst)]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source'); p.add_argument('destination')
    p.add_argument('--genre', choices=tuple(GENRE_ACCENTS), default='ai_work')
    p.add_argument('--fontfile', default=None)
    p.add_argument('--preset', default='veryfast')
    p.add_argument('--crf', type=int, default=19)
    a = p.parse_args()
    render(a.source, a.destination, a.genre, fontfile=a.fontfile, preset=a.preset, crf=a.crf)
