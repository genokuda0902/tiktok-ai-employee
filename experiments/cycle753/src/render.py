"""Cycle 753: cue-timed semantic animations on top of inherited slide video.

The input contains third-party/previous-cycle materials; human rights review is
mandatory before publication. No posting, upload, or paid services are used.
"""
from __future__ import annotations
import argparse
import json
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np

W, H, FPS = 1080, 1920, 30


def validate(config):
    c = config['canvas']
    assert (c['width'], c['height'], c['fps']) == (W, H, FPS)
    safe = config['caption_safe_y']
    assert 900 <= safe <= 1250
    spans = set()
    for cue in config['animations']:
        assert 0 <= cue['start_frame'] < cue['end_frame'] <= 429
        for frame in range(cue['start_frame'], cue['end_frame']):
            assert frame not in spans, 'overlapping cue spans'
            spans.add(frame)
        if cue['type'] == 'circuit_current':
            assert len(cue['path']) >= 2
            assert 4 <= cue['radius'] <= 20
            for x, y in cue['path']:
                assert 30 <= x <= 1050 and 350 <= y <= safe-120
        elif cue['type'] == 'led_emission':
            x, y = cue['center']
            assert 30 <= x <= 1050 and 350 <= y <= safe-120
            assert 30 <= cue['max_radius'] <= 130
        else:
            raise ValueError('unsupported animation type')
    return len(spans)


def eased(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def position_on_polyline(points, t):
    pts = np.asarray(points, dtype=np.float64)
    d = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    length = np.sum(d)
    traveled = float(np.clip(t, 0, 1)) * length
    for i, segment in enumerate(d):
        if traveled <= segment or i == len(d) - 1:
            p = pts[i] + (pts[i+1]-pts[i]) * traveled / max(segment, 1e-6)
            return tuple(np.rint(p).astype(int))
        traveled -= segment
    return tuple(pts[-1].astype(int))


def composite_glow(frame, center, radius, strength, color=(145, 245, 160)):
    """Bounded additive light with local ROI only; BGR color."""
    x, y = center
    r = int(max(8, radius*2.5))
    x0, x1 = max(0, x-r), min(W, x+r+1)
    y0, y1 = max(0, y-r), min(H, y+r+1)
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.ogrid[y0:y1, x0:x1]
    sigma = max(4, radius*.68)
    alpha = (strength*np.exp(-((xx-x)**2+(yy-y)**2)/(2*sigma**2))).astype(np.float32)
    roi = frame[y0:y1, x0:x1].astype(np.float32)
    roi += alpha[:, :, None]*np.asarray(color, dtype=np.float32)[None, None, :]
    frame[y0:y1, x0:x1] = np.clip(roi, 0, 255).astype(np.uint8)


def apply_cue(frame, idx, config):
    out = frame.copy()
    cue = next((c for c in config['animations'] if c['start_frame'] <= idx < c['end_frame']), None)
    if cue is None:
        return out
    duration = cue['end_frame'] - cue['start_frame']
    t = (idx-cue['start_frame'])/max(1,duration-1)
    if cue['type'] == 'circuit_current':
        # A travelling current dot, not an inaccurate recreation of real electron flow.
        pos = position_on_polyline(cue['path'], eased(t))
        composite_glow(out, pos, 30, .45, (160, 255, 165))
        cv2.circle(out, pos, cue['radius'], (165, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(out, pos, cue['radius']+5, (75, 170, 140), 2, cv2.LINE_AA)
    elif cue['type'] == 'led_emission':
        center = tuple(cue['center'])
        intensity = .26 + .12*math.sin(2*math.pi*t)
        composite_glow(out, center, cue['max_radius'], intensity, (110, 255, 170))
        cv2.circle(out, center, 16, (170, 255, 235), -1, cv2.LINE_AA)
        cv2.circle(out, center, int(26+cue['max_radius']*.5*eased(t)), (85, 220, 190), 2, cv2.LINE_AA)
        cv2.circle(out, center, int(28+cue['max_radius']*.8*eased(t)), (55, 150, 130), 1, cv2.LINE_AA)
    return out


def render(source, target, config):
    animated = validate(config)
    if not source.exists() or source.resolve() == target.resolve():
        raise ValueError('invalid source/target')
    cap = cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise RuntimeError('cannot open source')
    assert (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) == (W,H)
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error',
           '-f','rawvideo','-pixel_format','bgr24','-video_size',f'{W}x{H}',
           '-framerate',str(FPS),'-i','pipe:0','-i',str(source),
           '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast',
           '-crf','17','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy',
           '-movflags','+faststart',str(target)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    frames = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            proc.stdin.write(apply_cue(frame, frames, config).tobytes())
            frames += 1
        proc.stdin.close()
        err = proc.stderr.read().decode('utf-8','replace')
        code = proc.wait(timeout=240)
        if code:
            raise RuntimeError(f'ffmpeg failed {code}: {err[-1000:]}')
    finally:
        cap.release()
        if proc.poll() is None:
            proc.kill()
    if frames != 429 or not target.exists() or target.stat().st_size < 100_000:
        raise RuntimeError(f'incomplete video: {frames} frames')
    return {'frames':frames,'semantic_frames':animated,'output_bytes':target.stat().st_size}


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=root/'input/previous.mp4')
    parser.add_argument('--output', type=Path, default=root/'output/cycle753_SEMANTIC_LED_HUMAN_REVIEW.mp4')
    parser.add_argument('--config', type=Path, default=root/'config/semantic_cues.json')
    parser.add_argument('--genre', default='雑学・科学')
    args = parser.parse_args()
    genres = json.loads((root/'config/genres.json').read_text(encoding='utf-8'))
    if args.genre not in [g['name'] for g in genres['genres']]:
        raise ValueError('unsupported genre')
    cfg = json.loads(args.config.read_text(encoding='utf-8'))
    if cfg['genre'] != args.genre:
        raise ValueError('cue set is not authored for this genre')
    print(json.dumps(render(args.source,args.output,cfg),ensure_ascii=False))

if __name__ == '__main__':
    main()
