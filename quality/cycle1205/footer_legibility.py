#!/usr/bin/env python3
"""Offline footer microtext readability for 1080x1920 TikTok slide videos.

Thresholded luma-only lift in the disclaimer/footer region; never alters
narration, subtitles, main illustration, progress bar or source wording.
No network, publishing, paid service, personal data or automatic merge.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

FPS = 30
ROI = (64, 1730, 952, 144)
GENRE_PROFILES = {
    'ai': (58, 1.25), 'business': (58, 1.23), 'money': (60, 1.22),
    'learning': (56, 1.25), 'health': (60, 1.20), 'food': (60, 1.20),
    'travel': (60, 1.20), 'beauty': (62, 1.18), 'career': (58, 1.24),
    'life': (60, 1.20),
}

def probe(path):
    p = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
        capture_output=True, text=True, check=True
    )
    return json.loads(p.stdout)

def validate_source(info):
    v = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
    a = next((s for s in info['streams'] if s['codec_type'] == 'audio'), None)
    if not v or not a:
        raise ValueError('Input requires video and audio')
    if (v.get('codec_name'), int(v['width']), int(v['height']), v['r_frame_rate']) != ('h264', 1080, 1920, '30/1'):
        raise ValueError('Expected H264 1080x1920 30fps')
    if a.get('codec_name') != 'aac':
        raise ValueError('Expected AAC for bitstream copy')
    return int(v.get('nb_frames') or round(float(info['format']['duration']) * FPS))

def validate_roi(roi):
    if len(roi) != 4 or any(not isinstance(x, int) for x in roi):
        raise ValueError('ROI must be four integers')
    x, y, w, h = roi
    if x < 48 or x + w > 1032 or y < 1708 or y + h > 1890 or w < 300 or h < 50 or any(i % 2 for i in roi):
        raise ValueError('Footer ROI outside safe footer band or not even-aligned')
    return roi

def build_filter(roi=ROI, threshold=58, gain=1.25):
    x, y, w, h = validate_roi(roi)
    if not 48 <= threshold <= 80 or not 1.05 <= gain <= 1.35:
        raise ValueError('Unsafe luma profile')
    expr = f'if(gte(val,{threshold}),min(235,val*{gain:.3f}),val)'
    return (
        f'[0:v]split=2[base][ftr];'
        f'[ftr]crop={w}:{h}:{x}:{y},lutyuv=y=\'{expr}\'[lift];'
        f'[base][lift]overlay={x}:{y}:shortest=1:format=auto[outv]'
    )

def render(src, dst, genre='ai', frames=None, crf=16):
    if genre not in GENRE_PROFILES:
        raise ValueError('Unknown genre')
    total = validate_source(probe(src))
    if frames is not None:
        if not 1 <= frames <= total:
            raise ValueError('Invalid frame count')
        total = frames
    if not 14 <= crf <= 22:
        raise ValueError('CRF out of safe range')
    threshold, gain = GENRE_PROFILES[genre]
    filt = build_filter(ROI, threshold, gain)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(src),
        '-filter_complex', filt, '-map', '[outv]', '-map', '0:a:0',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf), '-pix_fmt', 'yuv420p',
        '-r', '30', '-fps_mode', 'cfr', '-c:a', 'copy', '-frames:v', str(total),
        '-movflags', '+faststart', '-metadata:s:a:0', 'language=jpn', str(dst)
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError('FFmpeg: ' + p.stderr[-2000:])
    return {'genre': genre, 'roi': ROI, 'threshold': threshold, 'gain': gain,
            'frames': total, 'output': str(dst)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('output')
    ap.add_argument('--genre', choices=sorted(GENRE_PROFILES), default='ai')
    ap.add_argument('--frames', type=int, default=None)
    ap.add_argument('--crf', type=int, default=16)
    args = ap.parse_args()
    print(json.dumps(render(args.source, args.output, args.genre, args.frames, args.crf),
                     ensure_ascii=False))

if __name__ == '__main__':
    main()
