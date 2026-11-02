#!/usr/bin/env python3
"""Offline quality-gated H.264 rate control for 1080x1920 Japanese narrated slides."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

GENRES = ('ai', 'business', 'money', 'learning', 'health', 'food',
          'travel', 'beauty', 'career', 'life')
WIDTH, HEIGHT, FPS = 1080, 1920, 30
PANEL = (52, 430, 824, 694)
FULL_SSIM_FLOOR = 0.996
PANEL_SSIM_FLOOR = 0.992

def command(args):
    result = subprocess.run([str(x) for x in args], capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace')[-1600:])
    return result

def probe(path):
    return json.loads(command(['ffprobe', '-v', 'error', '-show_streams',
                               '-show_chapters', '-show_format', '-of', 'json', path]).stdout)

def streams(meta):
    return (next(s for s in meta['streams'] if s['codec_type'] == 'video'),
            next(s for s in meta['streams'] if s['codec_type'] == 'audio'))

def aac_hash(path):
    data = command(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:a:0',
                    '-c:a', 'copy', '-f', 'adts', 'pipe:1']).stdout
    return hashlib.sha256(data).hexdigest()

def ssim_score(before, after, panel=None):
    if panel:
        x, y, w, h = panel
        graph = f'[0:v]crop={w}:{h}:{x}:{y}[a];[1:v]crop={w}:{h}:{x}:{y}[b];[a][b]ssim'
    else:
        graph = '[0:v][1:v]ssim'
    result = command(['ffmpeg', '-hide_banner', '-i', before, '-i', after,
                      '-filter_complex', graph, '-an', '-f', 'null', '-'])
    match = re.search(rb'SSIM Y:[\d.]+.*?All:([\d.]+)', result.stderr)
    if not match:
        raise RuntimeError('FFmpeg did not return an SSIM summary')
    return float(match.group(1))

def validate_source(path):
    meta = probe(path)
    video, audio = streams(meta)
    if (video.get('codec_name'), video.get('width'), video.get('height'),
        video.get('r_frame_rate'), audio.get('codec_name')) != ('h264', WIDTH, HEIGHT, '30/1', 'aac'):
        raise ValueError('Expected H264/AAC 1080x1920 30fps source')
    if not video.get('nb_frames'):
        raise ValueError('Missing source frame count')
    return meta

def encode(source, output, genre='ai', crf=21, verify_quality=True, report=None):
    if genre not in GENRES:
        raise ValueError('Unsupported genre')
    if not isinstance(crf, int) or not 16 <= crf <= 24:
        raise ValueError('CRF must be integer 16..24')
    source, output = Path(source), Path(output)
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError('Source missing or output equals input')
    before = validate_source(source)
    v, a = streams(before)
    count = int(v['nb_frames'])
    output.parent.mkdir(parents=True, exist_ok=True)
    command(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', source,
             '-map', '0:v:0', '-map', '0:a:0', '-map_chapters', '0',
             '-c:v', 'libx264', '-preset', 'medium', '-crf', str(crf),
             '-x264-params', 'aq-mode=3:aq-strength=1.0',
             '-pix_fmt', 'yuv420p', '-frames:v', str(count),
             '-c:a', 'copy', '-movflags', '+faststart', output])
    after = probe(output)
    ov, oa = streams(after)
    if (ov['width'], ov['height'], ov['r_frame_rate'], int(ov['nb_frames'])) != (WIDTH, HEIGHT, '30/1', count):
        raise RuntimeError('Output video frame geometry mismatch')
    if oa['codec_name'] != 'aac':
        raise RuntimeError('Output audio not AAC')
    if len(before.get('chapters', [])) != len(after.get('chapters', [])):
        raise RuntimeError('Chapters changed')
    if aac_hash(source) != aac_hash(output):
        raise RuntimeError('Japanese narration AAC bytes changed')
    command(['ffmpeg', '-v', 'error', '-xerror', '-i', output,
             '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'])
    full = ssim_score(source, output) if verify_quality else None
    panel = ssim_score(source, output, PANEL) if verify_quality else None
    if verify_quality and (full < FULL_SSIM_FLOOR or panel < PANEL_SSIM_FLOOR):
        raise RuntimeError(f'Quality gate failed: full={full} panel={panel}')
    result = {
        'genre': genre, 'genres_supported': len(GENRES), 'crf': crf,
        'preset': 'medium', 'dark_region_aq': 'aq-mode=3:aq-strength=1.0',
        'source_bytes': source.stat().st_size, 'output_bytes': output.stat().st_size,
        'size_change_percent': round(100 * (output.stat().st_size / source.stat().st_size - 1), 2),
        'frames': count, 'fps': FPS, 'resolution': [WIDTH, HEIGHT],
        'chapters': len(after.get('chapters', [])),
        'duration_s': float(after['format']['duration']),
        'aac_bitstream_identical': True, 'full_av_decode': 'PASS',
        'full_ssim': full, 'central_panel_ssim': panel,
        'full_ssim_floor': FULL_SSIM_FLOOR, 'central_panel_ssim_floor': PANEL_SSIM_FLOOR,
        'subtitle_text_content': 'NOT VERIFIED BY INDEPENDENT ASR',
        'subtitle_visual': 'PRESERVED IN VIDEO; QUALITY GATED BY SSIM',
        'source_rights': 'NOT VERIFIED', 'smartphone_device': 'NOT VERIFIED',
        'publication': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
    }
    if report:
        Path(report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source'); parser.add_argument('output')
    parser.add_argument('--genre', choices=GENRES, default='ai')
    parser.add_argument('--crf', type=int, default=21)
    parser.add_argument('--skip-quality-gate', action='store_true')
    parser.add_argument('--report')
    args = parser.parse_args()
    print(json.dumps(encode(args.source, args.output, args.genre, args.crf,
                            not args.skip_quality_gate, args.report),
                     ensure_ascii=False, indent=2))
