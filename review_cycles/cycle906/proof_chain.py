"""Cycle906: three-step evidence chain, review-only visual enhancement.

This is a NEW implementation, not original v33 source. The provided media stays
local. The generated animation contains fictional example values only and never
certifies that the underlying numbers have been independently checked.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work', 'business', 'education', 'finance', 'health',
          'lifestyle', 'technology', 'travel', 'food', 'entertainment')
STEPS = ('元データ', 'AIの下書き', '人が照合')
FPS = 30
TOTAL_FRAMES = 691
START_FRAME = 340
END_FRAME = 420
OVERLAY_WIDTH = 980
OVERLAY_HEIGHT = 98
CAPTION_START_Y = 1400
OVERLAY_TOP = 1200
REVIEW_STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run(args):
    p = subprocess.run(args, text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError('failed command: ' + repr(args[:6]) + '\n' + p.stderr[-2500:])
    return p.stdout


def validate_manifest(manifest):
    if manifest.get('genre') not in GENRES:
        raise ValueError('unsupported genre')
    for field in ('publication_approved', 'employee_approval', 'asset_rights_approved',
                  'upload_media_to_github', 'automatic_posting', 'paid_service'):
        if manifest.get(field) is not False:
            raise ValueError(field + ' must explicitly be false')
    if manifest.get('contains_private_data') is not False:
        raise ValueError('source must be privacy-reviewed before this review render')
    if manifest.get('caption_semantics_verified') is not False:
        raise ValueError('cannot claim semantic verification')
    if manifest.get('independent_japanese_asr_verified') is not False:
        raise ValueError('cannot claim ASR verification')
    digest = manifest.get('source_sha256')
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
        raise ValueError('valid source SHA256 required')
    if not isinstance(manifest.get('genre'), str):
        raise ValueError('genre required')
    return True


def font(size, bold=False):
    paths = ([
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    ] if bold else [
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    ])
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise RuntimeError('Japanese Noto Sans CJK font missing')


def active_step(frame_index):
    if not 0 <= frame_index <= END_FRAME - START_FRAME:
        raise ValueError('frame outside proof-chain window')
    return min(2, (frame_index * 3) // (END_FRAME - START_FRAME + 1))


def frame_image(frame_index):
    """Small RGBA ribbon, never writes in caption/HUD region."""
    stage = active_step(frame_index)
    im = Image.new('RGBA', (OVERLAY_WIDTH, OVERLAY_HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 979, 97), radius=20, fill=(2, 14, 32, 231), outline=(60, 150, 181, 228), width=2)
    f = font(27, bold=True)
    for i, label in enumerate(STEPS):
        x0 = 18 + i * 322
        x1 = x0 + 285
        is_current = i == stage
        done = i < stage
        fill = (8, 122, 139, 255) if is_current else ((18, 68, 79, 244) if done else (18, 33, 52, 242))
        outline = (105, 238, 231, 255) if is_current else (59, 106, 128, 255)
        d.rounded_rectangle((x0, 12, x1, 86), radius=15, fill=fill, outline=outline, width=3 if is_current else 1)
        prefix = '✓ ' if done else ('● ' if is_current else '○ ')
        label_text = prefix + label
        bbox = d.textbbox((0, 0), label_text, font=f)
        text_w = bbox[2] - bbox[0]
        d.text((x0 + (285-text_w)/2, 27), label_text, font=f,
               fill=(255, 255, 255, 255) if is_current else (191, 220, 228, 255), stroke_width=0)
        if i < 2:
            d.text((x1 + 8, 27), '›', font=f, fill=(102, 216, 218, 255))
    ramp = min(1., (frame_index + 1) / 8., (END_FRAME - START_FRAME - frame_index + 1) / 8.)
    if ramp < 1:
        alpha = im.getchannel('A').point(lambda a: round(a * ramp))
        im.putalpha(alpha)
    return im


def make_frames(directory, count=None):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    count = END_FRAME - START_FRAME + 1 if count is None else count
    if count < 1 or count > END_FRAME - START_FRAME + 1:
        raise ValueError('bad frame count')
    for i in range(count):
        frame_image(i).save(directory / f'frame_{i:03d}.png', optimize=True)
    return count


def media_info(path):
    info = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    video = next((s for s in info['streams'] if s['codec_type'] == 'video'), {})
    audio = next((s for s in info['streams'] if s['codec_type'] == 'audio'), {})
    return video, audio, info['format']


def validate_video(path):
    v, a, fmt = media_info(path)
    if (v.get('codec_name'), v.get('width'), v.get('height'), v.get('r_frame_rate'), int(v.get('nb_frames') or 0)) != ('h264', 1080, 1920, '30/1', TOTAL_FRAMES):
        raise ValueError('video must be H264 1080x1920 30fps 691 frames')
    if (a.get('codec_name'), a.get('sample_rate')) != ('aac', '48000'):
        raise ValueError('audio must be AAC 48kHz')
    return {'video_codec': v['codec_name'], 'audio_codec': a['codec_name'],
            'resolution': [v['width'], v['height']], 'fps': 30,
            'frames': int(v['nb_frames']), 'duration': float(fmt['duration'])}


def aac_sha(path, temp_dir):
    dest = Path(temp_dir) / (Path(path).stem + '.aac')
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(path), '-vn', '-c:a', 'copy', '-f', 'adts', str(dest)])
    return sha256(dest)


def render(source, output, manifest_path, workdir):
    import tempfile
    source, output = Path(source).resolve(), Path(output).resolve()
    if source == output or output.exists():
        raise ValueError('never overwrite original or existing output')
    manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    validate_manifest(manifest)
    if sha256(source) != manifest['source_sha256']:
        raise ValueError('source hash mismatch')
    validate_video(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    frames_dir = Path(workdir) / 'frames'
    make_frames(frames_dir)
    if OVERLAY_TOP + OVERLAY_HEIGHT >= CAPTION_START_Y:
        raise AssertionError('subtitle area would be overlaid')
    graph = (f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START_FRAME}/{FPS}/TB[proof];'
             f'[0:v][proof]overlay=50:{OVERLAY_TOP}:eof_action=pass:shortest=0:format=auto[v]')
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(source), '-framerate', str(FPS),
         '-start_number', '0', '-i', str(frames_dir / 'frame_%03d.png'),
         '-filter_complex', graph, '-map', '[v]', '-map', '0:a:0',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
         '-c:a', 'copy', '-frames:v', str(TOTAL_FRAMES), '-movflags', '+faststart', str(output)])
    meta = validate_video(output)
    run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'])
    with tempfile.TemporaryDirectory() as td:
        same_audio = aac_sha(source, td) == aac_sha(output, td)
    if not same_audio:
        raise AssertionError('audio bitstream changed')
    return {'status': REVIEW_STATUS, 'genre': manifest['genre'], 'source_sha256': sha256(source),
            'output_sha256': sha256(output), 'audio_bitstream_identical': same_audio,
            'full_av_decode': True, 'overlay_start_frame': START_FRAME,
            'overlay_end_frame': END_FRAME, 'overlay_frame_count': END_FRAME - START_FRAME + 1,
            'overlay_caption_safe': OVERLAY_TOP + OVERLAY_HEIGHT < CAPTION_START_Y,
            'subtitle_semantic_match': 'NOT_VERIFIED', 'independent_japanese_asr': 'NOT_AVAILABLE',
            'rights_approval': False, 'employee_approval': False,
            'public_posting_allowed': False, **meta}


def publication_gate(_report):
    raise PermissionError('PUBLICATION_NOT_APPROVED: ASR, rights, employee approval and device playback missing')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source'); p.add_argument('--output'); p.add_argument('--manifest')
    p.add_argument('--workdir'); p.add_argument('--report')
    p.add_argument('--smoke-frames', type=int)
    args = p.parse_args()
    if args.smoke_frames:
        make_frames(args.workdir, args.smoke_frames)
        print('smoke frames:', args.smoke_frames)
        return
    if not all((args.source, args.output, args.manifest, args.workdir, args.report)):
        p.error('render requires --source --output --manifest --workdir --report')
    result = render(args.source, args.output, args.manifest, args.workdir)
    Path(args.report).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
