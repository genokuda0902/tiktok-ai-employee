#!/usr/bin/env python3
"""Subtle main-diagram detail restoration for review-only 1080x1920 slides.

Applies a bounded FFmpeg unsharp/contrast pass to the main content panel.
Header, narration subtitles, footer and AAC bitstream are left untouched by
this filter. Ten genres share the engine; each may supply a custom panel ROI.
This does not establish text correctness, image rights or publication readiness.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

GENRES = {
    'ai': (.80, 1.065), 'business': (.75, 1.055),
    'money': (.78, 1.060), 'learning': (.85, 1.065),
    'health': (.62, 1.040), 'food': (.55, 1.035),
    'travel': (.55, 1.035), 'beauty': (.45, 1.025),
    'career': (.72, 1.050), 'life': (.60, 1.040),
}
DEFAULT_ROI = (60, 390, 960, 930)  # x, y, width, height
RESOLUTION = (1080, 1920)


def probe(path):
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_streams',
                        '-show_format', '-show_chapters', '-of', 'json', str(path)],
                       check=True, text=True, capture_output=True)
    return json.loads(p.stdout)


def validate(meta, genre, roi):
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    x, y, w, h = roi
    if any(not isinstance(v, int) for v in roi) or min(x, y) < 0 or min(w, h) <= 0:
        raise ValueError('invalid ROI')
    # Keep header and narration/footer untouched. Must fit 4:2:0 chroma grid.
    if x < 40 or y < 350 or x + w > 1040 or y + h > 1330 or any(v % 2 for v in roi):
        raise ValueError('ROI crosses protected header, subtitle or footer region')
    videos = [s for s in meta['streams'] if s.get('codec_type') == 'video']
    audios = [s for s in meta['streams'] if s.get('codec_type') == 'audio']
    if len(videos) != 1 or not audios or audios[0].get('codec_name') != 'aac':
        raise ValueError('requires one video stream and AAC audio')
    v = videos[0]
    if (int(v['width']), int(v['height'])) != RESOLUTION:
        raise ValueError('requires 1080x1920 source')
    if v.get('r_frame_rate') != '30/1':
        raise ValueError('requires constant 30 fps source')
    return int(v['nb_frames'])


def filter_graph(genre, roi):
    x, y, w, h = roi
    sharpen, contrast = GENRES[genre]
    return (f'[0:v]split[base][detailin];'
            f'[detailin]crop={w}:{h}:{x}:{y},'
            f'unsharp=5:5:{sharpen:.2f}:3:3:0.0,'
            f'eq=contrast={contrast:.3f}:saturation=1.020[detail];'
            f'[base][detail]overlay={x}:{y}:shortest=1,format=yuv420p[v]')


def render(source, target, genre='ai', roi=DEFAULT_ROI):
    source, target = Path(source), Path(target)
    if source.resolve() == target.resolve():
        raise ValueError('cannot overwrite source')
    meta = probe(source)
    nframes = validate(meta, genre, roi)
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y',
           '-i', str(source), '-filter_complex', filter_graph(genre, roi),
           '-map', '[v]', '-map', '0:a:0', '-map_metadata', '0', '-map_chapters', '0',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17',
           '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-frames:v', str(nframes),
           '-movflags', '+faststart', str(target)]
    subprocess.run(cmd, check=True)
    out = probe(target)
    out_frames = int(next(s for s in out['streams'] if s['codec_type'] == 'video')['nb_frames'])
    if out_frames != nframes:
        raise RuntimeError(f'frame mismatch: {out_frames} != {nframes}')
    return {'genre': genre, 'roi': roi, 'frames': nframes,
            'source_duration_s': float(meta['format']['duration']),
            'output_duration_s': float(out['format']['duration']),
            'sharpen': GENRES[genre][0], 'contrast': GENRES[genre][1],
            'subtitle_semantics_verified': False, 'publish_approved': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('source', type=Path)
    ap.add_argument('target', type=Path)
    ap.add_argument('--genre', choices=GENRES, default='ai')
    ap.add_argument('--roi', type=int, nargs=4, default=DEFAULT_ROI)
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    report = render(args.source, args.target, args.genre, tuple(args.roi))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False))
