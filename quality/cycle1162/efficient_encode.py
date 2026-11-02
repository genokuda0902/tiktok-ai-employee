#!/usr/bin/env python3
"""Review-only H264 size optimization with audio and subtitle-region quality gates.

Never publishes source media. This is not original v33 source or speech ASR.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = ('ai', 'business', 'money', 'learning', 'health', 'food', 'travel', 'beauty', 'career', 'life')
FULL_SSIM_MIN = 0.990
CAPTION_SSIM_MIN = 0.990
MAX_SIZE_RATIO = 0.70
CAPTION_CROP = 'crop=1080:600:0:1280'


def run(cmd, capture=False):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                          stderr=subprocess.PIPE, text=False)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def probe(path):
    info = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                           '-of', 'json', str(path)], True).stdout)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (v['codec_name'], int(v['width']), int(v['height']), v['avg_frame_rate']) != ('h264', 1080, 1920, '30/1'):
        raise ValueError('Expected H264 1080x1920 30fps')
    if (a['codec_name'], int(a['sample_rate'])) != ('aac', 48000):
        raise ValueError('Expected AAC 48kHz')
    return {'duration': float(info['format']['duration']), 'frames': int(v.get('nb_frames') or 0),
            'size': Path(path).stat().st_size}


def audio_sha(path):
    b = run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
             '-c:a', 'copy', '-f', 'adts', 'pipe:1'], True).stdout
    return hashlib.sha256(b).hexdigest()


def ssim(source, output, crop=False):
    filt = '[0:v]'+CAPTION_CROP+'[a];[1:v]'+CAPTION_CROP+'[b];[a][b]ssim' if crop else '[0:v][1:v]ssim'
    p = run(['ffmpeg', '-hide_banner', '-loglevel', 'info', '-i', str(source), '-i', str(output),
             '-filter_complex', filt, '-an', '-f', 'null', '-'], True)
    match = re.search(rb'SSIM Y:[^\n]*All:([0-9.]+)', p.stderr)
    if not match:
        raise RuntimeError('Missing SSIM metric')
    return float(match.group(1))


def validate_manifest(m, source):
    if (m.get('policy') != POLICY or m.get('asset_approval') != 'review_only_no_publication'
            or m.get('manual_post_only') is not True or m.get('genre') not in GENRES
            or m.get('layout_id') != 'eight_scene_v1'):
        raise ValueError('Fail closed: policy, genre or layout')
    if m.get('source_sha256') != sha256(source):
        raise ValueError('Fail closed: source SHA mismatch')


def render(source, output, manifest, report, smoke=False):
    source, output, manifest, report = map(Path, (source, output, manifest, report))
    if source.resolve() == output.resolve():
        raise ValueError('Cannot overwrite source')
    m = json.loads(manifest.read_text(encoding='utf-8'))
    validate_manifest(m, source)
    before = probe(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
         '-map', '0:v:0', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'medium',
         '-crf', '21', '-pix_fmt', 'yuv420p', '-threads', '4', '-c:a', 'copy',
         '-movflags', '+faststart', str(output)])
    after = probe(output)
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(output), '-f', 'null', '-'])
    full = ssim(source, output)
    caption = ssim(source, output, crop=True)
    audio_equal = audio_sha(source) == audio_sha(output)
    ratio = after['size'] / before['size']
    max_ratio = 0.95 if smoke else MAX_SIZE_RATIO
    passed = (before['frames'] == after['frames'] and before['frames'] > 0
              and abs(before['duration']-after['duration']) < 0.05
              and ratio <= max_ratio and full >= FULL_SSIM_MIN
              and caption >= CAPTION_SSIM_MIN and audio_equal)
    result = {'policy': POLICY, 'genre': m['genre'], 'source_sha256': sha256(source),
              'output_sha256': sha256(output), 'before': before, 'after': after,
              'size_ratio': ratio, 'full_ssim': full, 'caption_ssim': caption,
              'audio_adts_bit_identical': audio_equal, 'full_av_decode': True,
              'quality_gates_pass': passed, 'japanese_asr_verified': False,
              'spoken_caption_semantics_verified': False, 'rights_approved': False,
              'publication_approved': False}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    if not passed:
        output.unlink(missing_ok=True)
        raise RuntimeError('Quality gate FAILED: see report')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for arg in ('source', 'output', 'manifest', 'report'):
        p.add_argument('--'+arg, required=True)
    p.add_argument('--smoke', action='store_true')
    a = p.parse_args()
    print(json.dumps(render(a.source, a.output, a.manifest, a.report, a.smoke), indent=2))
