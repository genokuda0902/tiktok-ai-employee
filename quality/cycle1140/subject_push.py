#!/usr/bin/env python3
"""Review-only subject-local cinematic push/pull; not original v33."""
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = ('ai', 'business', 'money', 'learning', 'health', 'food', 'travel', 'beauty', 'career', 'life')

def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f'{argv[0]} exit={p.returncode}: {p.stderr[-1400:]}')
    return p.stdout

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def probe(path):
    d = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    v = [s for s in d['streams'] if s['codec_type'] == 'video']
    a = [s for s in d['streams'] if s['codec_type'] == 'audio']
    if len(v) != 1 or len(a) != 1 or any(s['codec_type'] == 'subtitle' for s in d['streams']):
        raise ValueError('require exactly one video and one audio, no soft subtitle')
    if v[0]['codec_name'] != 'h264' or (v[0]['width'], v[0]['height'], v[0]['avg_frame_rate']) != (1080, 1920, '30/1'):
        raise ValueError('expected H264 1080x1920 30fps')
    if a[0]['codec_name'] != 'aac' or a[0]['sample_rate'] != '48000' or a[0].get('tags', {}).get('language') != 'jpn':
        raise ValueError('expected AAC 48kHz tagged jpn')
    return {'frames': int(v[0]['nb_frames']), 'duration': float(d['format']['duration'])}

def validate(m, source_hash, spec):
    if set(m) != {'policy', 'asset_approval', 'source_sha256', 'genre', 'roi', 'start_frame', 'motion_frames', 'max_zoom', 'feather_px', 'title_guard_px'}:
        raise ValueError('unexpected or missing manifest fields')
    if m['policy'] != POLICY or m['asset_approval'] != 'private_review_only' or m['source_sha256'] != source_hash:
        raise ValueError('approval policy / source hash mismatch')
    if m['genre'] not in GENRES:
        raise ValueError('unsupported genre')
    roi = m['roi']
    if not isinstance(roi, dict) or set(roi) != {'x', 'y', 'width', 'height'} or any(type(v) != int for v in roi.values()):
        raise ValueError('invalid ROI')
    x, y, w, h = (roi[k] for k in ('x', 'y', 'width', 'height'))
    if not (60 <= x <= 300 and 470 <= y <= 650 and 300 <= w <= 850 and 250 <= h <= 525 and x+w <= 1010 and y+h <= 1000):
        raise ValueError('ROI crosses protected UI/caption boundary')
    st, n = m['start_frame'], m['motion_frames']
    if type(st) != int or type(n) != int or not (0 <= st <= 8 and 30 <= n <= 64 and st+n+2 < spec['frames']):
        raise ValueError('invalid motion frame range')
    if type(m['max_zoom']) not in (int, float) or not (1.025 <= m['max_zoom'] <= 1.10):
        raise ValueError('zoom outside safe range')
    if type(m['feather_px']) != int or not (16 <= m['feather_px'] <= 45):
        raise ValueError('invalid feather')
    if type(m['title_guard_px']) != int or not (80 <= m['title_guard_px'] <= 130):
        raise ValueError('title guard required to protect overhanging header callout')
    return x, y, w, h, st, n

def eased_zoom(progress, max_zoom):
    if not 0 <= progress <= 1:
        raise ValueError('progress outside [0,1]')
    return 1.0 + (max_zoom - 1.0) * math.sin(math.pi * progress) ** 2

def local_frame(image, roi, zoom, feather, title_guard):
    x, y, w, h = roi
    crop = image.crop((x, y, x+w, y+h)).convert('RGB')
    ww = int(round(w*zoom))
    hh = int(round(h*zoom))
    enlarged = crop.resize((ww, hh), Image.Resampling.LANCZOS)
    dx = (ww-w)//2
    dy = (hh-h)//2
    enlarged = enlarged.crop((dx, dy, dx+w, dy+h))
    xx = np.minimum(np.arange(w), np.arange(w)[::-1]).astype(np.float32)
    yy = np.minimum(np.arange(h), np.arange(h)[::-1]).astype(np.float32)
    edge = np.minimum(yy[:, None], xx[None, :])
    alpha = np.clip(edge/feather, 0, 1)
    # The title's small Japanese callout extends into the nominal subject ROI.
    guard = np.clip((np.arange(h, dtype=np.float32)-title_guard)/45, 0, 1)[:, None]
    alpha = alpha * guard
    alpha = alpha*alpha*(3-2*alpha)
    rgba = np.empty((h, w, 4), dtype=np.uint8)
    rgba[:, :, :3] = np.asarray(enlarged)
    rgba[:, :, 3] = (alpha*255).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')

def render(source, output, manifest, report):
    source = Path(source)
    output = Path(output)
    spec = probe(source)
    x, y, w, h, st, n = validate(manifest, digest(source), spec)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='subject_push_') as td:
        td = Path(td)
        frames = td/'frames'
        over = td/'overlay'
        frames.mkdir()
        over.mkdir()
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
             '-frames:v', str(st+n+1), '-start_number', '0', str(frames/'f_%03d.png')])
        blank = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        for i in range(st):
            blank.save(over/f'p_{i:03d}.png')
        for j in range(n):
            p = j/(n-1)
            z = eased_zoom(p, manifest['max_zoom'])
            if j in (0, n-1):
                blank.save(over/f'p_{st+j:03d}.png')
            else:
                image = Image.open(frames/f'f_{st+j:03d}.png').convert('RGB')
                local_frame(image, (x, y, w, h), z, manifest['feather_px'], manifest['title_guard_px']).save(over/f'p_{st+j:03d}.png', compress_level=1)
        blank.save(over/f'p_{st+n:03d}.png')
        run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
             '-framerate', '30', '-start_number', '0', '-i', str(over/'p_%03d.png'),
             '-filter_complex', f'[0:v][1:v]overlay=x={x}:y={y}:eof_action=pass:repeatlast=0:format=auto[v]',
             '-map', '[v]', '-map', '0:a:0', '-frames:v', str(spec['frames']),
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17',
             '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-metadata:s:a:0', 'language=jpn',
             '-movflags', '+faststart', str(output)])
    final = probe(output)
    if final['frames'] != spec['frames'] or abs(final['duration']-spec['duration']) > .04:
        raise RuntimeError('frame/duration mismatch')
    run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'])
    result = {'policy': POLICY, 'source_sha256': digest(source), 'output_sha256': digest(output),
              'frames': final['frames'], 'duration': final['duration'], 'fps': 30,
              'resolution': [1080, 1920], 'roi': [x, y, w, h],
              'motion_frames': n, 'max_zoom': manifest['max_zoom'],
              'title_guard_px': manifest['title_guard_px'],
              'technique': 'subject-only eased push/pull; protected text untouched',
              'audio': 'AAC jpn 48kHz stream copied', 'caption_semantics': 'NOT_VERIFIED',
              'phone_playback': 'NOT_VERIFIED'}
    Path(report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('source', 'output', 'manifest', 'report'):
        p.add_argument('--'+name, required=True)
    a = p.parse_args()
    print(json.dumps(render(a.source, a.output, json.loads(Path(a.manifest).read_text()), a.report), ensure_ascii=False, indent=2))
