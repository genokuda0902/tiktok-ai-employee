"""Move review-only provenance out of TikTok's lower UI danger zone.

Uses original footage and copy-muxed AAC; never grants publication approval.
Ten reusable genre palettes. Works with ffmpeg and installed CJK fonts.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess

GENRE_ACCENTS = {
    'ai': '39c6b8', 'business': '5e9fe1', 'finance': 'e4b966',
    'career': 'a88fe6', 'learning': '74c7a3', 'health': '74b6ce',
    'lifestyle': 'd99fae', 'travel': '77c7db', 'food': 'f0b47a',
    'news': 'b5b9cf',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BADGE = (570, 482, 460, 43)
DANGER_Y = 1710

def validate_geometry(width=1080, height=1920, badge=BADGE, danger_y=DANGER_Y):
    x, y, w, h = badge
    if (width, height) != (1080, 1920):
        raise ValueError('Fail closed: 1080x1920 required')
    if not (550 <= x and 475 <= y and x + w <= 1040 and y + h <= 532):
        raise ValueError('Badge must remain in verified empty top-middle gap')
    if not (1700 <= danger_y <= 1720):
        raise ValueError('Danger-zone cover must not touch narration subtitles')
    return True

def filter_graph(genre='ai', font=FONT):
    validate_geometry()
    if genre not in GENRE_ACCENTS:
        raise ValueError(f'Unsupported genre: {genre}')
    if not Path(font).is_file():
        raise FileNotFoundError(font)
    accent = GENRE_ACCENTS[genre]
    return ','.join([
        f'drawbox=x=0:y={DANGER_Y}:w=iw:h=ih-{DANGER_Y}:color=0x030711@1.0:t=fill',
        'drawbox=x=570:y=482:w=460:h=43:color=0x081c27@0.94:t=fill',
        f'drawbox=x=570:y=482:w=460:h=43:color=0x{accent}@0.8:t=2',
        f"drawtext=fontfile={font}:text='架空データ・社員承認前・投稿禁止':fontsize=22:fontcolor=0xe5f6f4:x=590:y=489:fix_bounds=1",
    ])

def render(src, dst, genre='ai', preset='fast', crf=21):
    src, dst = Path(src), Path(dst)
    if not src.is_file():
        raise FileNotFoundError(src)
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
    p.add_argument('src')
    p.add_argument('dst')
    p.add_argument('--genre', default='ai', choices=sorted(GENRE_ACCENTS))
    a = p.parse_args()
    print(render(a.src, a.dst, a.genre))
