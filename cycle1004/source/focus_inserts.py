#!/usr/bin/env python3
"""Four caption-safe content-focus bracket cues; never alters source audio or captions.

All coordinates are in normalized visual-only ROI, excluding top title and lower
Japanese captions. This is a private, review-only reimplementation, not v33.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import cv2

GENRES = ('ai_work', 'business', 'money', 'learning', 'health', 'life',
          'travel', 'food', 'tech', 'history')
# Windows deliberately avoid cycle1000's Calc zoom at 6.35-8.50 s.
AI_WORK_INSERTS = (
    (3.78, 4.62, 0.56, 0.48, 'repeated_task_human'),
    (9.35, 10.38, 0.55, 0.56, 'prompt_entry'),
    (12.28, 13.40, 0.53, 0.57, 'source_chart'),
    (18.24, 19.42, 0.52, 0.57, 'reusable_prompt'),
)
ROI = (70, 520, 1010, 1330)  # x0,y0,x1,y1; subtitle region starts below 1490
MAX_ZOOM = 1.0  # no zoom: text must never be cropped

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def validate(genre, windows, approved=False):
    if genre not in GENRES:
        raise ValueError('genre must be in ten-genre allowlist')
    if approved:
        raise ValueError('public release not supported; review-only')
    if genre != 'ai_work':
        raise ValueError('other genres require separately reviewed focus windows')
    prev = -1
    for start, end, cx, cy, label in windows:
        if not (0 <= start < end <= 23.0334 and end - start >= .35 and start >= prev):
            raise ValueError('invalid or overlapping focus windows')
        if not (.25 <= cx <= .75 and .25 <= cy <= .75 and label):
            raise ValueError('unsafe focus center or empty label')
        prev = end
    if len(windows) != 4:
        raise ValueError('exactly four reviewed insert windows required')

def focus_strength(t, start, end):
    if not start <= t < end:
        return 0.
    # 0.12-second ramps, never crossfades or double exposure.
    ramp = min(.12, (end - start) / 4)
    return max(0., min(1., (t-start)/ramp, (end-t)/ramp))

def focus_roi(frame, strength, cx, cy):
    """Draw subtle focus brackets; never crop or magnify Japanese UI text."""
    if strength <= 0:
        return frame
    x0, y0, x1, y1 = ROI
    w, h = x1-x0, y1-y0
    px, py = int(x0 + cx*w), int(y0 + cy*h)
    rx, ry = 245, 155
    left, right = max(x0+5, px-rx), min(x1-5, px+rx)
    top, bottom = max(y0+5, py-ry), min(y1-5, py+ry)
    length = 44
    glow = (102, 221, 175)  # BGR pale cyan
    bright = (205, 249, 228)
    thickness = max(1, int(round(5*strength)))
    for x, sign in ((left,1),(right,-1)):
        for y, vsign in ((top,1),(bottom,-1)):
            cv2.line(frame, (x,y), (x+sign*length,y), glow, thickness+3, cv2.LINE_AA)
            cv2.line(frame, (x,y), (x,y+vsign*length), glow, thickness+3, cv2.LINE_AA)
            cv2.line(frame, (x,y), (x+sign*length,y), bright, thickness, cv2.LINE_AA)
            cv2.line(frame, (x,y), (x,y+vsign*length), bright, thickness, cv2.LINE_AA)
    return frame

def probe(path):
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                        '-of', 'json', str(path)], check=True, capture_output=True, text=True)
    return json.loads(p.stdout)

def render(source, output, report, genre='ai_work', review_only=False):
    validate(genre, AI_WORK_INSERTS)
    if not review_only:
        raise ValueError('review-only flag required')
    source, output, report = Path(source), Path(output), Path(report)
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError('invalid source/output')
    meta = probe(source)
    streams = meta['streams']
    video = next(s for s in streams if s['codec_type'] == 'video')
    audio = next((s for s in streams if s['codec_type'] == 'audio'), None)
    subs = next((s for s in streams if s['codec_type'] == 'subtitle'), None)
    if (video['width'], video['height'], video['r_frame_rate']) != (1080, 1920, '30/1'):
        raise ValueError('must be 1080x1920 at 30fps')
    if not audio or audio.get('sample_rate') != '48000' or not subs:
        raise ValueError('Japanese audio and selectable subtitles required')
    cap = cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise RuntimeError('cannot decode source')
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
           '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1080x1920', '-r', '30',
           '-i', 'pipe:0', '-i', str(source), '-map', '0:v:0', '-map', '1:a:0',
           '-map', '1:s:0', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '19',
           '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-c:s', 'copy',
           '-metadata:s:a:0', 'language=jpn', '-metadata:s:s:0', 'language=jpn',
           '-movflags', '+faststart', str(output)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    count = changed = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            t = count / 30
            for start, end, cx, cy, label in AI_WORK_INSERTS:
                strength = focus_strength(t, start, end)
                if strength:
                    focus_roi(frame, strength, cx, cy)
                    changed += 1
                    break
            proc.stdin.write(frame.tobytes())
            count += 1
    finally:
        cap.release()
        if proc.stdin:
            proc.stdin.close()
    err = proc.stderr.read().decode('utf8', errors='replace')
    if proc.wait() != 0:
        raise RuntimeError('ffmpeg failed: ' + err[-1500:])
    if count != 691:
        raise ValueError('expected exactly 691 frames')
    result = {'source_sha256': sha(source), 'output_sha256': sha(output),
              'genre': genre, 'frames': count, 'focus_frames': changed,
              'windows': [list(w) for w in AI_WORK_INSERTS], 'max_zoom': MAX_ZOOM, 'text_cropping': False,
              'protected_roi': {'top_title': 'y<520', 'caption': 'y>=1330',
                                'left_right_margin': 70},
              'review_only': True, 'publication_approved': False,
              'independent_japanese_asr': 'NOT_AVAILABLE',
              'audio_caption_semantic_match': 'NOT_VERIFIED'}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--genre', default='ai_work')
    parser.add_argument('--review-only', action='store_true')
    args = parser.parse_args()
    print(json.dumps(render(args.source, args.output, args.report,
                            args.genre, args.review_only), ensure_ascii=False))
