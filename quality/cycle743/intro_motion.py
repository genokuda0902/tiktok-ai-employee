"""cycle743: reproducible ten-genre animated proof panel for a review-only MP4.

All sales data are fictional; this is an illustrated interface, not a recording.
Uses no third-party media. Requires Pillow, ffmpeg, and an approved source MP4.
"""
from __future__ import annotations
import argparse
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = {
    'ai_work': '#3ce8ee', 'sales': '#ffb650', 'business': '#8eb2ff',
    'finance': '#a6e684', 'career': '#ff92b6', 'study': '#c8acff',
    'health': '#6de0a5', 'travel': '#72caff', 'food': '#ffbe66',
    'lifestyle': '#ff9ed6',
}
VALUES = (12, 15, 20, 18)
LABELS = ('1月', '2月', '3月', '4月')
FPS, FRAMES = 30, 96
X, Y, W, H = 60, 590, 498, 435
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def progress(t: float, index: int) -> float:
    """Staggered cubic ease-out, clamped to [0,1]."""
    v = min(1.0, max(0.0, (t - 0.22 - index * 0.58) / 0.75))
    return 1 - (1-v)**3

def render_panel(t: float, genre: str = 'ai_work') -> Image.Image:
    if genre not in GENRES:
        raise ValueError('unknown genre')
    color = tuple(bytes.fromhex(GENRES[genre][1:]))
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = lambda n: ImageFont.truetype(FONT, n)
    d.rounded_rectangle((0, 0, W-1, H-1), radius=35,
                        fill=(10, 32, 58, 255), outline=(135, 208, 237, 255), width=4)
    d.rounded_rectangle((19, 20, 480, 82), radius=22, fill=(22, 65, 96, 255))
    for j, rgb in enumerate(((252,122,117), (250,203,107), (106,222,181))):
        d.ellipse((45+j*35, 45, 60+j*35, 60), fill=rgb+(255,))
    d.text((175, 28), '月別売上', font=font(32), fill='white')
    complete = 0
    for j, (label, value) in enumerate(zip(LABELS, VALUES)):
        p = progress(t, j)
        complete += value if p >= 1 else 0
        yy = 104 + j * 70
        d.text((46, yy), label, font=font(29), fill=(220, 237, 247, 255))
        d.rounded_rectangle((158, yy+4, 398, yy+36), radius=10, fill=(37, 72, 96, 255))
        width = round(value * 11 * p)
        if width >= 3:
            d.rounded_rectangle((158, yy+4, 158+width, yy+36), radius=min(10,width//2), fill=color+(255,))
        d.text((399, yy), f'{value}万' if p >= .99 else '…', font=font(25), fill=(245,251,255,255))
    d.line((41, 386, 453, 386), fill=(108,176,212,155), width=2)
    done = all(progress(t, i) >= .999 for i in range(4))
    text = '合計 65万円  ※架空データ' if done else '集計中…  ※架空データ'
    d.text((41, 393), text, font=font(24), fill=(205,230,244,255))
    return im

def build_overlays(folder: Path, genre: str = 'ai_work') -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for i in range(FRAMES):
        render_panel(i/FPS, genre).save(folder/f'{i:03d}.png', optimize=True)

def encode(source: Path, folder: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y',
           '-i',str(source),'-framerate',str(FPS),'-i',str(folder/'%03d.png'),
           '-filter_complex',f'[0:v][1:v]overlay={X}:{Y}:enable=lt(t\\,3.2):shortest=0,format=yuv420p[v]',
           '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
           '-crf','20','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--genre',choices=tuple(GENRES),default='ai_work')
    p.add_argument('--overlay-dir',type=Path,required=True)
    a=p.parse_args()
    build_overlays(a.overlay_dir,a.genre)
    encode(a.source,a.overlay_dir,a.output)
