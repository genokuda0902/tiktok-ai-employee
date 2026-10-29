#!/usr/bin/env python3
"""Review-only transition ghost repair. No private assets leave the local machine.

Replace a short *upper-artwork-only* range with a verified later clean frame.
The original lower Japanese-caption region and original AAC are inherited.
Other genres require explicit scene-coordinate review and fail closed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image

FPS = 30
WIDTH, HEIGHT = 1080, 1920
CAPTION_SAFE_Y = 1440
DEFAULT_START, DEFAULT_END, DEFAULT_ANCHOR = 522, 530, 532
GENRES = ('ai_work', 'finance', 'learning', 'health', 'travel', 'food', 'science', 'history', 'business', 'lifestyle')


def run(args, *, capture=False):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for part in iter(lambda: f.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def validate_plan(genre, synthetic, start, end, anchor, total):
    if genre not in GENRES:
        raise ValueError('Unknown genre: fail closed')
    if genre != 'ai_work' and not synthetic:
        raise ValueError('Unreviewed genre layout: fail closed')
    if not (0 <= start <= end < anchor < total):
        raise ValueError('Invalid repair/anchor frame sequence')
    if end - start + 1 > 15:
        raise ValueError('Repair window too long: manual review required')
    if anchor - end > 6:
        raise ValueError('Clean anchor too distant: manual review required')


def probe(path):
    p = run(['ffprobe', '-v', 'error', '-show_entries',
             'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
             '-show_entries', 'format=duration', '-of', 'json', str(path)], capture=True)
    data = json.loads(p.stdout)
    vs = [s for s in data['streams'] if s['codec_type'] == 'video']
    audio = [s for s in data['streams'] if s['codec_type'] == 'audio']
    if len(vs) != 1 or not audio:
        raise ValueError('Exactly one video stream and an audio stream are required')
    v = vs[0]
    if (v['width'], v['height'], v['r_frame_rate']) != (WIDTH, HEIGHT, '30/1'):
        raise ValueError('Unreviewed source resolution or frame rate')
    count = int(v.get('nb_frames') or round(float(data['format']['duration']) * FPS))
    return count, data


def extract_anchor(source, anchor, work):
    frame = work / 'anchor_full.png'
    # Decode by absolute frame number; avoid seeking/keyframe drift.
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
         '-vf', f'select=eq(n\\,{anchor})', '-vsync', '0', '-frames:v', '1', str(frame)])
    if not frame.is_file():
        raise RuntimeError('Clean anchor extraction failed')
    top = work / 'clean_top.png'
    with Image.open(frame) as im:
        if im.size != (WIDTH, HEIGHT):
            raise ValueError('Unexpected anchor dimensions')
        im.convert('RGB').crop((0, 0, WIDTH, CAPTION_SAFE_Y)).save(top)
    return top


def repair(source, output, work, *, genre='ai_work', synthetic=False,
           start=DEFAULT_START, end=DEFAULT_END, anchor=DEFAULT_ANCHOR):
    source, output, work = Path(source), Path(output), Path(work)
    if not source.is_file():
        raise FileNotFoundError(source)
    total, info = probe(source)
    validate_plan(genre, synthetic, start, end, anchor, total)
    work.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    top = extract_anchor(source, anchor, work)
    filtergraph = (f"[0:v][1:v]overlay=0:0:enable='between(n,{start},{end})':"
                   'eof_action=pass:format=auto[v]')
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
         '-loop', '1', '-framerate', str(FPS), '-i', str(top),
         '-filter_complex', filtergraph, '-map', '[v]', '-map', '0:a:0',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19',
         '-pix_fmt', 'yuv420p', '-r', str(FPS), '-frames:v', str(total),
         '-c:a', 'copy', '-movflags', '+faststart', str(output)])
    output_count, _ = probe(output)
    if output_count != total:
        raise RuntimeError(f'Frame count changed {total} -> {output_count}')
    return dict(source_sha256=sha256(source), output_sha256=sha256(output),
                frame_count=total, repaired_frames=end-start+1,
                repair_range=[start,end], clean_anchor=anchor,
                caption_safe_y=CAPTION_SAFE_Y, genre=genre,
                synthetic_only=synthetic, publication_approved=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--genre', default='ai_work')
    ap.add_argument('--synthetic', action='store_true')
    ap.add_argument('--start', type=int, default=DEFAULT_START)
    ap.add_argument('--end', type=int, default=DEFAULT_END)
    ap.add_argument('--anchor', type=int, default=DEFAULT_ANCHOR)
    args = ap.parse_args()
    report = repair(args.source,args.output,args.work,genre=args.genre,synthetic=args.synthetic,
                    start=args.start,end=args.end,anchor=args.anchor)
    print(json.dumps(report, ensure_ascii=False, indent=2))
