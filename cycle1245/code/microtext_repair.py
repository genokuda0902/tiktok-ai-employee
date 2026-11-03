"""Repair a hard-to-read baked-in microcaption in a 1080x1920 slideshow.

Uses only original user-review footage, FFmpeg and a locally installed CJK font.
Confined to the bottom caption strip of the illustration panel of chapter 2 (3.20-5.67s).
Ten-genre color palette; no changes to speech, subtitle panel, or disclosure.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess

PALETTE = {
    'ai':'69d5cb','business':'8abef2','finance':'e4b966',
    'career':'b7a1ec','learning':'82d7b0','health':'84c7dd',
    'lifestyle':'e6b0bd','travel':'8ad7ea','food':'efbb89',
    'news':'c9cedd',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
START, END = 3.20, 5.67
RECT = (90, 1242, 750, 58)
TEXT = 'まずは繰り返し作業を書き出す'


def validate(genre, width=1080, height=1920, font=FONT):
    if genre not in PALETTE:
        raise ValueError('Unknown genre')
    if (width, height) != (1080, 1920):
        raise ValueError('Only 1080x1920 is supported')
    if not Path(font).is_file():
        raise FileNotFoundError(font)
    x,y,w,h=RECT
    if not (3.0 < START < END < 5.7 and 70 <= x and x+w <= 875 and 1230 <= y and y+h <= 1310):
        raise ValueError('Overlay outside illustration-safe region')
    return True


def filter_graph(genre='ai', font=FONT):
    validate(genre, font=font)
    accent=PALETTE[genre]
    active=f'between(t\\,{START:.2f}\\,{END:.2f})'
    x,y,w,h=RECT
    return ','.join([
        f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0x071c26@0.98:t=fill:enable=\'{active}\'',
        f'drawbox=x={x}:y={y}:w=5:h={h}:color=0x{accent}@0.96:t=fill:enable=\'{active}\'',
        f'drawtext=fontfile={font}:text={TEXT}:fontsize=27:fontcolor=0xf2fbff:x={x+18}:y={y+12}:enable=\'{active}\':fix_bounds=1',
    ])


def render(source, output, genre='ai', preset='fast', crf=21):
    validate(genre)
    src,dst=Path(source),Path(output)
    if not src.is_file() or src.resolve()==dst.resolve():
        raise ValueError('Source must exist and differ from output')
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
        '-map','0:v:0','-map','0:a:0','-vf',filter_graph(genre),
        '-c:v','libx264','-preset',preset,'-crf',str(crf),'-pix_fmt','yuv420p',
        '-fps_mode','passthrough','-c:a','copy','-metadata:s:a:0','language=jpn',
        '-movflags','+faststart',str(dst)],check=True)
    return dst

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');
    p.add_argument('--genre',default='ai',choices=sorted(PALETTE));a=p.parse_args()
    print(render(a.source,a.output,a.genre))
