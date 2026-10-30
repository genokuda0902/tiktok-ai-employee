#!/usr/bin/env python3
"""Review-only shadow lift for portrait image-first shorts; never approves publication."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from PIL import Image

# A single renderer; the presets are conservative and never authorize media.
GENRE_GAMMA = {
    'ai_work': 1.18, 'business': 1.16, 'money': 1.14,
    'learning': 1.16, 'health': 1.12, 'life': 1.17,
    'travel': 1.10, 'food': 1.10, 'tech': 1.17, 'history': 1.16,
}
ROI = (24, 255, 1032, 1110)  # excludes top header, baked subtitles and footer
FADE = 36


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                           '-show_format', '-of', 'json', str(path)]).stdout)


def validate(meta, genre, review_only):
    if not review_only:
        raise ValueError('Explicit review-only gate is required')
    if genre not in GENRE_GAMMA:
        raise ValueError('Unknown genre')
    streams = meta['streams']
    video = next((s for s in streams if s['codec_type'] == 'video'), None)
    audio = next((s for s in streams if s['codec_type'] == 'audio'), None)
    if not video or video.get('width') != 1080 or video.get('height') != 1920:
        raise ValueError('Expected portrait 1080x1920 source')
    if not audio or audio.get('sample_rate') != '48000':
        raise ValueError('48kHz narration required')
    return True


def mask_image(path, w=ROI[2], h=ROI[3], fade=FADE):
    if fade < 1 or 2 * fade >= min(w, h):
        raise ValueError('Invalid feather width')
    from PIL import ImageDraw
    # Edge feather prevents visible rectangular seams on dark templates.
    img = Image.new('L', (w, h), 0)
    pixels = img.load()
    for y in range(h):
        fy = min(1., y / fade, (h - 1 - y) / fade)
        for x in range(w):
            fx = min(1., x / fade, (w - 1 - x) / fade)
            pixels[x, y] = round(255 * min(fx, fy))
    img.save(path)


def filtergraph(gamma):
    x, y, w, h = ROI
    if not 1.0 <= gamma <= 1.25:
        raise ValueError('Unsafe gamma')
    return (f'[0:v]split=2[base][lift];'
            f'[lift]crop={w}:{h}:{x}:{y},'
            f'eq=gamma={gamma}:gamma_weight=0.82:saturation=1.04,'
            f'format=rgb24[graded];'
            f'[1:v]format=gray[alpha];'
            f'[graded][alpha]alphamerge[masked];'
            f'[base][masked]overlay={x}:{y}:shortest=1:format=auto,'
            f'format=yuv420p[v]')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def render(source, output, genre, report, review_only=True, preset='veryfast'):
    source, output, report = map(Path, (source, output, report))
    if source.resolve() == output.resolve():
        raise ValueError('Never overwrite source')
    if not source.is_file():
        raise FileNotFoundError(source)
    meta = probe(source)
    validate(meta, genre, review_only)
    output.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='tonepass-') as temp:
        mask = Path(temp) / 'feather.png'
        mask_image(mask)
        command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                   '-i', str(source), '-framerate', '30', '-loop', '1', '-i', str(mask),
                   '-filter_complex', filtergraph(GENRE_GAMMA[genre]),
                   '-map', '[v]', '-map', '0:a:0']
        if any(s['codec_type'] == 'subtitle' for s in meta['streams']):
            command += ['-map', '0:s:0', '-c:s', 'copy',
                        '-metadata:s:s:0', 'language=jpn']
        command += ['-c:v', 'libx264', '-preset', preset, '-crf', '18',
                    '-pix_fmt', 'yuv420p', '-c:a', 'copy',
                    '-metadata:s:a:0', 'language=jpn',
                    '-frames:v', str(next(s for s in meta['streams'] if s['codec_type']=='video').get('nb_frames', '691')),
                    '-movflags', '+faststart', str(output)]
        run(command)
    after = probe(output)
    data = {'genre': genre, 'review_only': True, 'publication_approved': False,
            'independent_japanese_asr': False, 'gamma': GENRE_GAMMA[genre],
            'roi': ROI, 'feather': FADE, 'source_sha256': sha256(source),
            'output_sha256': sha256(output),
            'input_streams': [s['codec_name'] for s in meta['streams']],
            'output_streams': [s['codec_name'] for s in after['streams']],
            'duration_seconds': float(after['format']['duration'])}
    report.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    return data


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--report', required=True)
    p.add_argument('--genre', choices=sorted(GENRE_GAMMA), default='ai_work')
    p.add_argument('--preset', default='veryfast')
    p.add_argument('--review-only', action='store_true', required=True)
    args = p.parse_args()
    print(json.dumps(render(args.input, args.output, args.genre, args.report,
                            args.review_only, args.preset), ensure_ascii=False))
