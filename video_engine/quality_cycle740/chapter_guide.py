"""Review-only, 10-genre chapter navigator for an existing vertical MP4.

Uses no external assets; generated PNGs contain only original vector/text graphics.
Requires FFmpeg and Pillow. The input video's voice and captions are retained.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DURATION = 27.343
BREAKS = (0.0, 6.5, 12.8, 24.3, DURATION)
DEFAULT_LABELS = ('課題', '入力', '確認', '保存')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
PANEL_X, PANEL_Y, PANEL_W, PANEL_H = 930, 360, 130, 350


def validate(labels, breaks, duration):
    if len(labels) != 4 or any(not x or len(x) > 12 for x in labels):
        raise ValueError('Exactly four short chapter labels are required')
    if len(breaks) != 5 or abs(breaks[0]) > 1e-6 or abs(breaks[-1] - duration) > 0.05:
        raise ValueError('Chapter boundaries must span the full video')
    if any(b >= a for b, a in zip(breaks, breaks[1:])):
        raise ValueError('Chapter boundaries must increase')
    if PANEL_Y + PANEL_H > 1670 or PANEL_X < 40 or PANEL_X + PANEL_W > 1080:
        raise ValueError('Navigator outside conservative TikTok safe region')


def make_panel(index: int, labels=DEFAULT_LABELS):
    if index not in range(4):
        raise ValueError('index 0..3')
    im = Image.new('RGBA', (PANEL_W, PANEL_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, PANEL_W-4, PANEL_H-4), radius=30,
                        fill=(3, 23, 44, 205), outline=(93, 222, 226, 120), width=2)
    font = ImageFont.truetype(FONT, 28)
    small = ImageFont.truetype(FONT, 19)
    d.text((26, 15), f'{index+1}/4', font=font, fill=(120, 249, 239, 255))
    d.text((33, 54), '進行', font=small, fill=(210, 239, 247, 230))
    d.line((65, 103, 65, 305), fill=(77, 147, 161, 160), width=5)
    for j, label in enumerate(labels):
        y = 105 + j * 60
        active = j == index
        fill = (21, 197, 198, 255) if active else (29, 68, 93, 235)
        outline = (235, 255, 255, 255) if active else (112, 174, 190, 190)
        d.ellipse((41, y, 89, y+48), fill=fill, outline=outline, width=3)
        d.text((55 if j < 9 else 50, y+5), str(j+1), font=font,
               fill=(1, 24, 43, 255) if active else (204, 234, 242, 255))
    return im


def render(source: Path, output: Path, labels=DEFAULT_LABELS, breaks=BREAKS):
    validate(labels, breaks, DURATION)
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='chapter740_') as temp:
        panels = []
        for i in range(4):
            p = Path(temp)/f'panel{i}.png'
            make_panel(i, labels).save(p)
            panels.append(p)
        # Use the input video once, overlay four chapter cards only during their segment.
        args = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source)]
        for p in panels:
            args += ['-loop', '1', '-framerate', '30', '-i', str(p)]
        chain = []
        last = '[0:v]'
        for i in range(4):
            out = f'[v{i}]'
            chain.append(f"{last}[{i+1}:v]overlay={PANEL_X}:{PANEL_Y}:format=auto:shortest=1:enable='gte(t,{breaks[i]})*lt(t,{breaks[i+1]})'{out}")
            last = out
        args += ['-filter_complex', ';'.join(chain), '-map', last, '-map', '0:a:0',
                 '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
                 '-r', '30', '-t', str(DURATION), '-c:a', 'copy', '-movflags', '+faststart', str(output)]
        subprocess.run(args, check=True)
    return output


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--labels', nargs=4, default=list(DEFAULT_LABELS))
    a = ap.parse_args()
    render(a.source, a.output, a.labels)
    print(json.dumps({'output':str(a.output),'labels':a.labels,'boundaries':BREAKS},ensure_ascii=False))

if __name__ == '__main__':
    main()
