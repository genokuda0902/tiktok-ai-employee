#!/usr/bin/env python3
"""Review-only 10-genre legibility pass for a lower-content takeaway.

Never publishes or uploads source media. Audio is copied unchanged; subtitle
region below y=1500 is protected by a hard overlay-boundary invariant.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = {
    'ai': '#27d9d1', 'business': '#51c7f4', 'money': '#eac56c',
    'learning': '#8fc4ff', 'health': '#79d7ab', 'food': '#f3bd79',
    'travel': '#80c8e8', 'beauty': '#efafd2', 'career': '#93a5ff',
    'life': '#a7dfb0',
}
POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
WIDTH, HEIGHT, FPS = 1080, 1920, 30
X, Y, W, H = 50, 1095, 850, 132
CAPTION_START = 1500
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()

def check_manifest(data, source, duration):
    if data.get('policy') != POLICY or data.get('genre') not in GENRES:
        raise ValueError('Review-only policy or genre not authorized')
    if data.get('source_sha256') != sha256(source):
        raise ValueError('Source SHA256 mismatch; fail closed')
    title = data.get('takeaway')
    if not isinstance(title, str) or not 3 <= len(title) <= 18 or any(ord(c) < 32 for c in title):
        raise ValueError('Unsafe or overlong takeaway')
    start, end = data.get('start'), data.get('end')
    if not all(isinstance(v, (int, float)) for v in (start, end)) or not 0.3 < start < end < duration - 0.1 or end - start < 0.6:
        raise ValueError('Unsafe interval')
    if X < 0 or Y < 0 or X + W > WIDTH or Y + H >= CAPTION_START:
        raise ValueError('Overlay could touch captions')
    return title, float(start), float(end)

def probe(path):
    obj = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    v = next(x for x in obj['streams'] if x['codec_type'] == 'video')
    a = next(x for x in obj['streams'] if x['codec_type'] == 'audio')
    if (v['codec_name'], int(v['width']), int(v['height']), v['r_frame_rate']) != ('h264', WIDTH, HEIGHT, '30/1'):
        raise ValueError('Input must be H264 1080x1920 at 30fps')
    if a['codec_name'] != 'aac' or int(a['sample_rate']) != 48000:
        raise ValueError('Input must include AAC 48kHz')
    return float(obj['format']['duration']), int(v.get('nb_frames', 0) or 0)

def make_overlay(title, genre, path):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    accent = GENRES[genre]
    d.rounded_rectangle((2, 3, W-3, H-4), radius=22, fill=(4, 23, 39, 251), outline=accent, width=3)
    d.rounded_rectangle((16, 23, 147, 108), radius=14, fill=accent)
    lab = ImageFont.truetype(FONT, 25)
    headline = ImageFont.truetype(FONT, 43)
    d.text((33, 48), 'NEXT', font=lab, fill=(3, 29, 43, 255), stroke_width=0)
    bbox = d.textbbox((0, 0), title, font=headline)
    if bbox[2] > W - 190:
        raise ValueError('Takeaway exceeds safe width')
    d.text((178, 33), title, font=headline, fill=(255, 255, 255, 255), stroke_width=0)
    d.rounded_rectangle((178, 107, W-42, 112), radius=2, fill=accent)
    im.save(path)

def render(source, output, manifest, overlay_path=None):
    source, output = Path(source), Path(output)
    duration, frames = probe(source)
    data = json.loads(Path(manifest).read_text(encoding='utf-8'))
    title, start, end = check_manifest(data, source, duration)
    overlay = Path(overlay_path) if overlay_path else output.with_suffix('.overlay.png')
    make_overlay(title, data['genre'], overlay)
    fade = min(0.22, (end-start)/4)
    fc = (f'[1:v]format=rgba,fade=t=in:st={start:.3f}:d={fade:.3f}:alpha=1,'
          f'fade=t=out:st={end-fade:.3f}:d={fade:.3f}:alpha=1[plate];'
          f"[0:v][plate]overlay={X}:{Y}:format=auto:enable='between(t,{start:.3f},{end:.3f})'[v]")
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
           '-loop', '1', '-framerate', str(FPS), '-i', str(overlay),
           '-filter_complex', fc, '-map', '[v]', '-map', '0:a:0',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-threads', '2',
           '-pix_fmt', 'yuv420p', '-frames:v', str(frames or round(duration*FPS)),
           '-c:a', 'copy', '-movflags', '+faststart', str(output)]
    subprocess.run(cmd, check=True)
    out_duration, out_frames = probe(output)
    if frames and out_frames != frames:
        raise RuntimeError(f'Frame count mismatch: {frames} -> {out_frames}')
    if abs(out_duration - duration) > 0.06:
        raise RuntimeError('Duration changed')
    return {'source_sha256': sha256(source), 'output_sha256': sha256(output),
            'frames': out_frames, 'duration': out_duration, 'takeaway': title,
            'start': start, 'end': end, 'policy': POLICY}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--manifest', required=True)
    p.add_argument('--report', required=True)
    a = p.parse_args()
    result = render(a.source, a.output, a.manifest)
    Path(a.report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
