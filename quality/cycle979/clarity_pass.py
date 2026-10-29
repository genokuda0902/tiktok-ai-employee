#!/usr/bin/env python3
"""Cycle979 review-only edge clarity. No upload, posting, or paid service."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

WIDTH, HEIGHT, FPS = 1080, 1920, 30
ARTWORK_BOTTOM = 1180
GENRE_PROFILES = {
    'ai_work': .65, 'finance': .45, 'learning': .55,
    'health': .40, 'travel': .35, 'food': .30,
    'science': .55, 'history': .35, 'business': .55,
    'lifestyle': .35,
}

def run(args):
    return subprocess.run(args, check=True, capture_output=True).stdout

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-count_frames',
                           '-show_streams', '-show_format', '-of', 'json', str(path)]))

def validate(genre, synthetic=False):
    if genre not in GENRE_PROFILES:
        raise ValueError('Unknown genre')
    if genre != 'ai_work' and not synthetic:
        raise ValueError('Unreviewed genre layout: fail closed')
    return GENRE_PROFILES[genre]

def filter_graph(amount):
    return ('[0:v]split=2[base][art];'
            f'[art]crop={WIDTH}:{ARTWORK_BOTTOM}:0:0,'
            f'unsharp=5:5:{amount:.2f}:3:3:0[sharp];'
            '[base][sharp]overlay=0:0:format=auto:shortest=1[v]')

def render(source, output, genre='ai_work', synthetic=False):
    amount = validate(genre, synthetic)
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == output.resolve():
        raise ValueError('Output must not overwrite source')
    output.parent.mkdir(parents=True, exist_ok=True)
    info = probe(source)
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (video['width'], video['height'], video['r_frame_rate']) != (WIDTH, HEIGHT, '30/1'):
        raise ValueError('Expected 1080x1920 30fps input')
    if audio['codec_name'] != 'aac' or audio['sample_rate'] != '48000':
        raise ValueError('Expected AAC 48kHz source')
    frames = int(video['nb_read_frames'])
    if frames < 30:
        raise ValueError('Too few frames')
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
         '-i', str(source), '-filter_complex', filter_graph(amount),
         '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264',
         '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
         '-r', str(FPS), '-frames:v', str(frames), '-c:a', 'copy',
         '-movflags', '+faststart', str(output)])
    return {'cycle': 979, 'source_sha256': sha256(source),
            'output_sha256': sha256(output), 'genre': genre,
            'genres_configured': len(GENRE_PROFILES),
            'artwork_y': [0, ARTWORK_BOTTOM],
            'caption_protection_y': [ARTWORK_BOTTOM, HEIGHT],
            'sharpen_strength': amount, 'frames_expected': frames,
            'audio_mode': 'AAC stream copy',
            'review_state': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--genre', default='ai_work')
    p.add_argument('--synthetic', action='store_true')
    p.add_argument('--report')
    args = p.parse_args()
    result = render(args.source, args.output, args.genre, args.synthetic)
    if args.report:
        Path(args.report).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
