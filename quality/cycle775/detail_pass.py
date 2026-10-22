#!/usr/bin/env python3
"""Cycle775: free, generic artwork-only detail and chroma improvement.

Requires FFmpeg. Operates on licensed/approved source media only; never posts.
The voice, cue timings, footer and TikTok UI-safe caption zone are retained.
"""
import argparse
import json
import subprocess
from PIL import Image
from pathlib import Path

DEFAULTS = dict(contrast=1.055, saturation=1.065, sharpen=0.52, top=180, height=950)


def filtergraph(cfg):
    c, s, sharp = float(cfg['contrast']), float(cfg['saturation']), float(cfg['sharpen'])
    top, height = int(cfg['top']), int(cfg['height'])
    if not (1.0 <= c <= 1.12 and 1.0 <= s <= 1.15 and 0 <= sharp <= 0.8):
        raise ValueError('Detail settings outside conservative bounds')
    if top < 145 or height < 200 or top + height > 1170:
        raise ValueError('Enhancement must stay outside the subtitle and footer region')
    return (f'[0:v]split=2[base][work];'
            f'[work]crop=1080:{height}:0:{top},'
            f'eq=contrast={c}:saturation={s},'
            f'unsharp=5:5:{sharp}:5:5:0,format=yuv420p[detail];'
            f'[1:v]format=gray[mask];'
            f'[detail][mask]alphamerge[masked];'
            f'[base][masked]overlay=0:{top}:shortest=1:format=auto[v]')


def run(source, output, config=None):
    cfg = dict(DEFAULTS)
    if config:
        cfg.update(json.loads(Path(config).read_text(encoding='utf-8')))
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    import numpy as np
    h = int(cfg['height'])
    fade = 70
    ys = np.arange(h)
    alpha = np.minimum(1.0, np.minimum((ys+1)/fade, (h-ys)/fade))
    mask = np.tile(np.uint8(np.round(255*alpha))[:,None], (1,1080))
    mask_file = output.parent / 'feather_mask.png'
    Image.fromarray(mask, mode='L').save(mask_file)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
           '-loop','1','-framerate','30','-i',str(mask_file),
           '-filter_complex',filtergraph(cfg),'-map','[v]','-map','0:a:0',
           '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
           '-r','30','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return output

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--config')
    args = p.parse_args()
    print(run(args.source,args.output,args.config))
