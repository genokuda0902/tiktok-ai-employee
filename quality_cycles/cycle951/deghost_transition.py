"""Cycle951: deghost text-heavy scene boundaries with non-overlapping fade-through-solid.

Purely local, deterministic post-processing. Preserves source audio and publication gate.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np

FPS = 30
SCENE_CUTS = (2.8, 5.8, 8.7, 11.6, 14.5, 17.4, 20.3)
# Configurable 10-genre transition palettes. No user or third-party media is fetched.
GENRE_BACKGROUNDS = {
    "ai_work": (21, 11, 4), "business": (31, 21, 9),
    "finance": (22, 19, 9), "education": (24, 18, 12),
    "technology": (24, 15, 5), "health": (23, 21, 12),
    "travel": (32, 20, 12), "food": (29, 20, 16),
    "lifestyle": (28, 19, 13), "entertainment": (27, 12, 16),
}  # OpenCV BGR

def window(cut_s: float, fps: int = FPS) -> tuple[int, int]:
    """11-frame interval centered just after the cut, excluding stable neighboring frames."""
    cut = round(cut_s * fps)
    return cut - 4, cut + 7

def fade_alpha(frame_idx: int, start: int, end: int) -> float:
    """Opacity for one clean source at a time: no double exposure of text."""
    if not start <= frame_idx < end:
        raise ValueError('frame outside transition window')
    midpoint = (start + end - 1) / 2
    return float(0.10 + 0.90 * abs(frame_idx - midpoint) / max(1, (end - 1 - start) / 2))

def make_feather_mask(height: int, width: int, top_ratio: float = .078, bottom_ratio: float = .777) -> np.ndarray:
    """Protect top badge and bottom subtitle. Only scene text/art region is replaced."""
    top = round(height * top_ratio)
    bottom = round(height * bottom_ratio)
    mask = np.zeros((height, 1, 1), dtype=np.float32)
    mask[top+20:bottom-20] = 1
    for k in range(20):
        v = (k + 1) / 21
        mask[top+k] = v
        mask[bottom-20+k] = 1-v
    return mask

def render(input_mp4: Path, output_mp4: Path, genre: str, qa_path: Path):
    if genre not in GENRE_BACKGROUNDS:
        raise ValueError(f'unknown genre: {genre}')
    if input_mp4.resolve() == output_mp4.resolve():
        raise ValueError('cannot overwrite source')
    cap = cv2.VideoCapture(str(input_mp4))
    if not cap.isOpened():
        raise RuntimeError('source MP4 cannot be opened')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (width, height) != (1080, 1920) or abs(fps-FPS) > 0.01 or frames != 691:
        raise ValueError(f'unexpected source: {width}x{height}, {fps}fps, {frames} frames')
    windows = [window(t) for t in SCENE_CUTS]
    snapshots = {}
    for i, cut in enumerate(SCENE_CUTS):
        cut_frame = round(cut * FPS)
        for side, fi in [('pre', cut_frame - 10), ('post', cut_frame + 11)]:
            cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
            ok, fr = cap.read()
            if not ok:
                raise RuntimeError(f'could not load clean {side} frame {fi}')
            snapshots[(i, side)] = fr
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    video_tmp = output_mp4.with_suffix('.video_only.mp4')
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
           '-s',f'{width}x{height}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264',
           '-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(video_tmp)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    mask = make_feather_mask(height, width)
    dark = np.array(GENRE_BACKGROUNDS[genre], dtype=np.float32).reshape((1,1,3))
    changed = []
    try:
        for n in range(frames):
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError(f'decode failed at frame {n}')
            for i,(start,end) in enumerate(windows):
                if start <= n < end:
                    side = 'pre' if n < round(SCENE_CUTS[i]*FPS) else 'post'
                    alpha = fade_alpha(n,start,end)
                    snap = snapshots[(i,side)].astype(np.float32)
                    clean = snap * alpha + dark * (1-alpha)
                    mixed = clean * mask + frame.astype(np.float32) * (1-mask)
                    frame = np.uint8(np.clip(mixed,0,255))
                    changed.append(n)
                    break
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        err = proc.stderr.read().decode(errors='replace')
        rc = proc.wait()
        if rc:
            raise RuntimeError(f'video encoder failed: {err[-2000:]}')
    finally:
        cap.release()
        if proc.poll() is None:
            proc.kill()
    mux = subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video_tmp),
                          '-i',str(input_mp4),'-map','0:v:0','-map','1:a:0',
                          '-c:v','copy','-c:a','copy','-movflags','+faststart',str(output_mp4)],
                         capture_output=True,text=True)
    if mux.returncode:
        raise RuntimeError(f'audio mux failed: {mux.stderr[-2000:]}')
    video_tmp.unlink(missing_ok=True)
    report = {'cycle':951,'source':str(input_mp4),'output':str(output_mp4),'genre':genre,
              'cut_seconds':SCENE_CUTS,'changed_frame_count':len(changed),
              'changed_frame_indices':changed,'windows':windows,
              'protected': 'header top 7.8% and bottom subtitles below 77.7%',
              'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    qa_path.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--genre',choices=GENRE_BACKGROUNDS,default='ai_work')
    p.add_argument('--qa',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output,a.genre,a.qa),ensure_ascii=False)[:500])
