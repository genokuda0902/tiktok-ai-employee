"""Restrained opening-hook motion cue for Japanese 1080x1920 slides.

Only the first scene (0.22-1.32 s) is changed; audio is stream-copied.
Never treats the result as approved for publication.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess

GENRE_ACCENTS = {
    'ai': 'e9d389', 'business': '8abef2', 'finance': 'e4b966',
    'career': 'b7a1ec', 'learning': '82d7b0', 'health': '84c7dd',
    'lifestyle': 'e6b0bd', 'travel': '8ad7ea', 'food': 'efbb89',
    'news': 'c9cedd',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
OPEN_START, OPEN_END = 0.22, 1.32
X_START, X_END, Y = 84, 595, 434

def validate(genre: str, width=1080, height=1920, font=FONT):
    if (width, height) != (1080, 1920):
        raise ValueError('Fail closed: expected 1080x1920')
    if genre not in GENRE_ACCENTS:
        raise ValueError(f'Unknown genre: {genre}')
    if not Path(font).is_file():
        raise FileNotFoundError(font)
    if not (0 < OPEN_START < OPEN_END < 1.4 and X_START < X_END < 610 and Y < 465):
        raise ValueError('Hook cue geometry outside protected opening region')
    return True

def filter_graph(genre='ai', font=FONT):
    validate(genre, font=font)
    color = GENRE_ACCENTS[genre]
    phase = f'max(0\\,min(1\\,(t-{OPEN_START})/{OPEN_END-OPEN_START}))'
    easing = f'(1-pow(1-{phase}\\,3))'
    x = f'{X_START}+({X_END-X_START})*{easing}'
    return ','.join([
        f"drawtext=fontfile={font}:text='●':fontsize=29:fontcolor=0x{color}@0.23:x='{x}-5':y={Y-5}:enable='between(t\\,{OPEN_START}\\,{OPEN_END})':fix_bounds=1",
        f"drawtext=fontfile={font}:text='●':fontsize=17:fontcolor=0x{color}@0.98:x='{x}':y={Y}:enable='between(t\\,{OPEN_START}\\,{OPEN_END})':fix_bounds=1",
    ])

def render(src, dst, genre='ai', preset='fast', crf=21):
    validate(genre)
    src, dst = Path(src), Path(dst)
    if not src.is_file():
        raise FileNotFoundError(src)
    if src.resolve() == dst.resolve():
        raise ValueError('Source and output must differ')
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(src),
           '-map', '0:v:0', '-map', '0:a:0', '-vf', filter_graph(genre),
           '-c:v', 'libx264', '-preset', preset, '-crf', str(crf),
           '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough',
           '-c:a', 'copy', '-metadata:s:a:0', 'language=jpn',
           '-movflags', '+faststart', str(dst)]
    subprocess.run(cmd, check=True)
    return dst

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source')
    p.add_argument('output')
    p.add_argument('--genre', default='ai', choices=sorted(GENRE_ACCENTS))
    a = p.parse_args()
    print(render(a.source, a.output, a.genre))
