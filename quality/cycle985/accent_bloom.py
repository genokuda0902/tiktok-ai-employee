"""Cycle985: caption-safe accent-only light diffusion on image-slide art.

No rights or publication claim. All genre IDs supported; real-video layout
is approved for processing only for ai_work. Human publication review required.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np

GENRE_HUES = {
    'ai_work': (78, 103), 'money': (38, 77), 'health': (40, 95),
    'science': (90, 130), 'history': (8, 30), 'language': (120, 165),
    'career': (78, 110), 'psychology': (120, 170),
    'travel': (5, 32), 'lifestyle': (80, 125),
}
REVIEWED_LAYOUTS = {'ai_work'}


def validate(width, height, fps, genre, top, bottom, strength, synthetic=False):
    if genre not in GENRE_HUES:
        raise ValueError('Unknown genre')
    if genre not in REVIEWED_LAYOUTS and not synthetic:
        raise ValueError('Layout not reviewed: fail closed')
    if width < 64 or height < 128 or fps <= 0:
        raise ValueError('Invalid geometry')
    if not (0 <= top < bottom <= height - 200):
        raise ValueError('Caption protected region must be at least 200 px')
    if not (0 < strength <= 30):
        raise ValueError('Strength out of safety range')


def bloom_frame(frame, genre='ai_work', top=150, bottom=1180, strength=28):
    if frame.dtype != np.uint8 or frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError('Expected uint8 BGR frame')
    h, w = frame.shape[:2]
    validate(w, h, 30, genre, top, bottom, strength, synthetic=True)
    out = frame.copy()
    roi = out[top:bottom]
    scale = .25
    small = cv2.resize(roi, (max(16, round(w*scale)), max(16, round((bottom-top)*scale))), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    lo, hi = GENRE_HUES[genre]
    accent = cv2.inRange(hsv, (lo, 105, 110), (hi, 255, 255))
    near = cv2.GaussianBlur(accent, (0, 0), 3.5)
    far = cv2.GaussianBlur(accent, (0, 0), 10.0)
    glow = cv2.resize(cv2.addWeighted(near, .7, far, .3, 0), (w, bottom-top), interpolation=cv2.INTER_LINEAR)
    glow = (glow.astype(np.float32) / 255.0 * strength)
    for channel, factor in ((0, .75), (1, 1.0), (2, .28)):
        addition = (glow * factor).astype(np.uint8)
        roi[:, :, channel] = cv2.add(roi[:, :, channel], addition)
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()


def render(source, output, genre='ai_work', synthetic=False, top=150, bottom=1180, strength=28):
    src, dst = Path(source), Path(output)
    if src.resolve() == dst.resolve():
        raise ValueError('Do not overwrite source')
    cap = cv2.VideoCapture(str(src))
    if not cap.isOpened():
        raise RuntimeError('Input MP4 not readable')
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    validate(w, h, fps, genre, top, bottom, strength, synthetic)
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y',
           '-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}',
           '-r',str(fps),'-i','pipe:0','-i',str(src),
           '-map','0:v:0','-map','1:a:0','-c:v','libx264',
           '-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
           '-c:a','copy','-movflags','+faststart',str(dst)]
    with subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        count = 0
        try:
            while True:
                ok, frame = cap.read()
                if not ok: break
                processed = bloom_frame(frame, genre, top, bottom, strength)
                proc.stdin.write(processed.tobytes())
                count += 1
            proc.stdin.close()
            error = proc.stderr.read().decode('utf-8', errors='replace')
            rc = proc.wait()
            if rc != 0: raise RuntimeError(f'ffmpeg failed ({rc}): {error[-1000:]}')
        except Exception:
            proc.kill()
            proc.wait()
            raise
        finally:
            cap.release()
    return {'cycle':985, 'source_sha256':sha256(src), 'output_sha256':sha256(dst),
            'frames_processed':count, 'genre':genre, 'protected_caption_from_y':bottom,
            'strength':strength, 'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source'); p.add_argument('output')
    p.add_argument('--genre',default='ai_work'); p.add_argument('--synthetic',action='store_true')
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,args.synthetic),ensure_ascii=False,indent=2))
