#!/usr/bin/env python3
"""Review-only scene-boundary flash guard for ten-genre Japanese portrait shorts.

A deterministic, local-only reimplementation. No publication permission or asset upload.
Only applies short, feathered cross-dissolves to manifest-declared cuts with
large central-region luma discontinuities. Protected header/caption/footer untouched
at pixel-processing stage (codec re-encode may introduce small changes).
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import cv2
import numpy as np

GENRES = ('ai_work', 'business', 'money', 'learning', 'health', 'life',
          'travel', 'food', 'tech', 'history')
ROI = (24, 255, 1032, 855)  # top/center artwork; outside baked caption/footer
FADE_PIXELS = 36
RAMP = (0.28, 0.49, 0.70, 0.86, 1.0)
DEFAULT_THRESHOLD = 55.0


def command(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(command(['ffprobe', '-v', 'error', '-show_streams',
                               '-show_format', '-of', 'json', str(path)]))


def validate(meta, genre, review_only, cuts):
    if not review_only:
        raise ValueError('Review-only explicit gate required')
    if genre not in GENRES:
        raise ValueError('Unsupported genre: no implicit publication approval')
    video = next((s for s in meta['streams'] if s['codec_type'] == 'video'), None)
    audio = next((s for s in meta['streams'] if s['codec_type'] == 'audio'), None)
    sub = next((s for s in meta['streams'] if s['codec_type'] == 'subtitle'), None)
    if not video or (video.get('width'), video.get('height'), video.get('r_frame_rate')) != (1080, 1920, '30/1'):
        raise ValueError('1080x1920/30fps source required')
    if not audio or audio.get('sample_rate') != '48000':
        raise ValueError('48kHz narration required')
    if not sub:
        raise ValueError('Existing Japanese subtitle track required')
    frames = int(video.get('nb_frames', 0))
    if frames < 12 or not cuts or any(c < 1 or c + len(RAMP) >= frames for c in cuts):
        raise ValueError('Manifest cut indexes outside frame count')
    if cuts != sorted(set(cuts)):
        raise ValueError('Cuts must be sorted and unique')
    return frames


def luma(frame):
    x, y, w, h = ROI
    patch = frame[y:y+h:4, x:x+w:4]
    return float(cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY).mean())


def mask(w=ROI[2], h=ROI[3], feather=FADE_PIXELS):
    if feather < 1 or feather * 2 >= min(w, h):
        raise ValueError('Invalid feather')
    xs = np.minimum(np.arange(w), np.arange(w)[::-1]) / float(feather)
    ys = np.minimum(np.arange(h), np.arange(h)[::-1]) / float(feather)
    return np.minimum(1, np.minimum(ys[:, None], xs[None, :])).astype(np.float32)[:, :, None]


def blend_roi(previous, current, alpha, matte):
    if not (0 < alpha <= 1):
        raise ValueError('Invalid alpha')
    if alpha == 1:
        return current
    x, y, w, h = ROI
    result = current.copy()
    old = previous[y:y+h, x:x+w].astype(np.float32)
    new = current[y:y+h, x:x+w].astype(np.float32)
    mix = (new * alpha + old * (1-alpha)) * matte + new * (1-matte)
    result[y:y+h, x:x+w] = np.clip(np.rint(mix), 0, 255).astype(np.uint8)
    return result


def inspect_cuts(source, cuts, threshold):
    if threshold < 10 or threshold > 150:
        raise ValueError('Unsafe threshold')
    cap = cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise ValueError('Cannot open input video')
    changes = []
    for cut in cuts:
        cap.set(cv2.CAP_PROP_POS_FRAMES, cut - 1)
        ok0, prev = cap.read()
        ok1, nxt = cap.read()
        if not (ok0 and ok1):
            cap.release()
            raise ValueError('Cannot decode cut')
        before, after = luma(prev), luma(nxt)
        changes.append({'cut_frame': cut, 'before_luma': round(before, 3),
                        'after_luma': round(after, 3),
                        'jump': round(abs(after-before), 3),
                        'guarded': abs(after-before) >= threshold})
    cap.release()
    return changes


def render(source, output, report, genre, cuts, review_only=False,
           threshold=DEFAULT_THRESHOLD, preset='veryfast'):
    source, output, report = map(Path, (source, output, report))
    if source.resolve() == output.resolve():
        raise ValueError('Never overwrite source')
    if not source.is_file():
        raise FileNotFoundError(source)
    meta = probe(source)
    frames = validate(meta, genre, review_only, cuts)
    changes = inspect_cuts(source, cuts, threshold)
    guarded = {x['cut_frame'] for x in changes if x['guarded']}
    if not guarded:
        raise ValueError('No qualifying flash: fail closed instead of fake improvement')
    output.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(source))
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
           '-f', 'rawvideo', '-pixel_format', 'bgr24', '-video_size', '1080x1920',
           '-framerate', '30', '-i', 'pipe:0', '-i', str(source),
           '-map', '0:v:0', '-map', '1:a:0', '-map', '1:s:0',
           '-c:v', 'libx264', '-preset', preset, '-crf', '18', '-pix_fmt', 'yuv420p',
           '-c:a', 'copy', '-c:s', 'copy', '-metadata:s:a:0', 'language=jpn',
           '-metadata:s:s:0', 'language=jpn', '-frames:v', str(frames),
           '-movflags', '+faststart', str(output)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    matte = mask()
    last = None
    cut_anchor = None
    active_cut = None
    written = 0
    try:
        for i in range(frames):
            ok, frame = cap.read()
            if not ok:
                raise ValueError(f'Video decode ended at frame {i}')
            if i in guarded:
                cut_anchor = last.copy()
                active_cut = i
            if active_cut is not None and i - active_cut < len(RAMP):
                out_frame = blend_roi(cut_anchor, frame, RAMP[i-active_cut], matte)
            else:
                out_frame = frame
            proc.stdin.write(out_frame.tobytes())
            last = frame
            written += 1
        proc.stdin.close()
        err = proc.stderr.read().decode('utf-8', 'replace')
        if proc.wait() != 0:
            raise RuntimeError('FFmpeg render failed: '+err[-2000:])
    except Exception:
        if proc.stdin and not proc.stdin.closed:
            proc.stdin.close()
        proc.kill()
        proc.wait()
        raise
    finally:
        cap.release()
    after = probe(output)
    actual = int(next(s for s in after['streams'] if s['codec_type']=='video')['nb_frames'])
    if actual != written:
        raise RuntimeError(f'Frame count mismatch {actual} != {written}')
    data = {'genre':genre, 'review_only':True, 'publication_approved':False,
            'independent_japanese_asr':False, 'original_v33_comparison':False,
            'source_sha256':sha256(source), 'output_sha256':sha256(output),
            'frame_count':actual, 'duration_seconds':float(after['format']['duration']),
            'resolution':'1080x1920', 'fps':30, 'roi':ROI, 'ramp':RAMP,
            'threshold_luma':threshold, 'cut_results':changes,
            'guarded_cuts':sorted(guarded), 'audio_subtitle_reencoded':False}
    report.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--report', required=True)
    p.add_argument('--genre', default='ai_work')
    p.add_argument('--cuts', required=True, help='Comma-separated exact scene start frames')
    p.add_argument('--threshold', type=float, default=DEFAULT_THRESHOLD)
    p.add_argument('--preset', default='veryfast')
    p.add_argument('--review-only', action='store_true', required=True)
    a = p.parse_args()
    cuts = [int(x) for x in a.cuts.split(',')]
    print(json.dumps(render(a.input,a.output,a.report,a.genre,cuts,a.review_only,
                            a.threshold,a.preset),ensure_ascii=False))
