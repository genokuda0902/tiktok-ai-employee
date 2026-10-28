"""Cycle922: review-only, audio-activity timeline for an existing captioned MP4.

Does NOT transcribe Japanese or prove captions match speech. No uploads or posting.
The runtime uses local FFmpeg, OpenCV, NumPy, webrtcvad; CI tests pure helpers.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path

FPS = 30
SAMPLE_RATE = 16000
VAD_WINDOW_MS = 30
SCENE_BOUNDS = [0, 87, 174, 261, 348, 435, 522, 588, 691]
REVIEW_STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
GENRES = ('ai_work', 'finance', 'business', 'health', 'education', 'tech',
          'lifestyle', 'history', 'travel', 'productivity')


def scene_index(frame: int, bounds=SCENE_BOUNDS) -> int:
    if frame < bounds[0] or frame >= bounds[-1]:
        raise ValueError('frame outside video')
    return next(i for i in range(len(bounds) - 1) if bounds[i] <= frame < bounds[i + 1])


def time_to_vad_index(frame: int, fps: int = FPS, ms: int = VAD_WINDOW_MS) -> int:
    return max(0, int((frame / fps) * (1000 / ms)))


def smooth_vad(bits: list[bool], radius: int = 3) -> list[bool]:
    """Suppress isolated false speech spikes without changing underlying QA."""
    if radius < 0:
        raise ValueError('negative radius')
    return [sum(bits[max(0, i-radius):min(len(bits), i+radius+1)]) >=
            math.ceil((min(len(bits), i+radius+1)-max(0, i-radius))/2)
            for i in range(len(bits))]


def speech_coverage(bits: list[bool], bounds=SCENE_BOUNDS, fps: int = FPS,
                    ms: int = VAD_WINDOW_MS) -> list[float]:
    if not bits:
        raise ValueError('no audio activity available')
    ratios = []
    for start, end in zip(bounds[:-1], bounds[1:]):
        a, b = time_to_vad_index(start, fps, ms), time_to_vad_index(end, fps, ms)
        window = bits[a:min(len(bits), max(a+1, b))]
        if not window:
            raise ValueError('audio shorter than video')
        ratios.append(round(sum(window)/len(window), 4))
    return ratios


def render_safe_region() -> tuple[int, int]:
    # Existing burned Japanese caption text ends above y=1710; waveform 1710-1760.
    # Only redraw the original progress track below the waveform.
    return (1768, 1802)


def assert_review_only(genre: str, output: str) -> None:
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    if not output.endswith('_REVIEW_ONLY.mp4'):
        raise ValueError('review-only output naming required')


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def extract_vad(src: Path) -> tuple[list[bool], float]:
    import numpy as np
    import webrtcvad
    cmd = ['ffmpeg', '-v', 'error', '-i', str(src), '-vn', '-ac', '1',
           '-ar', str(SAMPLE_RATE), '-f', 's16le', 'pipe:1']
    raw = subprocess.run(cmd, check=True, stdout=subprocess.PIPE).stdout
    audio = np.frombuffer(raw, dtype='<i2')
    window = SAMPLE_RATE * VAD_WINDOW_MS // 1000
    vad = webrtcvad.Vad(2)
    bits = [vad.is_speech(audio[i:i+window].tobytes(), SAMPLE_RATE)
            for i in range(0, len(audio)-window+1, window)]
    return bits, len(audio) / SAMPLE_RATE


def draw_timeline(frame, frame_number: int, bits: list[bool], bounds=SCENE_BOUNDS):
    import cv2
    import numpy as np
    # Preserve all pixels above 1768: Japanese subtitle content and waveform.
    y0, y1 = render_safe_region()
    x0, x1 = 85, 869
    cv2.rectangle(frame, (x0-8, y0), (x1+8, y1), (30, 12, 2), -1)
    cv2.rectangle(frame, (x0, 1778), (x1, 1788), (70, 57, 30), -1)
    # Speech segments are shown as a faint map of the entire 23-second audio.
    for j, active in enumerate(bits):
        if not active:
            continue
        x = x0 + int(j * (x1-x0) / max(1, len(bits)-1))
        cv2.line(frame, (x, 1779), (x, 1787), (215, 196, 60), 1)
    for b in bounds[1:-1]:
        x = x0 + round(b / bounds[-1] * (x1-x0))
        cv2.line(frame, (x, 1775), (x, 1792), (108, 100, 82), 1)
    current_x = x0 + round(frame_number / (bounds[-1]-1) * (x1-x0))
    # Real-time marker distinguishes speech from silence (VAD heuristic only).
    active = bits[min(len(bits)-1, time_to_vad_index(frame_number))]
    color = (230, 231, 234) if active else (118, 119, 119)
    cv2.circle(frame, (current_x, 1783), 7, color, -1, cv2.LINE_AA)
    cv2.circle(frame, (current_x, 1783), 9, (20, 46, 56), 1, cv2.LINE_AA)
    return frame


def video_caption_presence(src: Path) -> list[float]:
    """Visual ink proxy only: cannot read Japanese words or verify semantics."""
    import cv2
    cap = cv2.VideoCapture(str(src))
    values = []
    for a, b in zip(SCENE_BOUNDS[:-1], SCENE_BOUNDS[1:]):
        cap.set(cv2.CAP_PROP_POS_FRAMES, (a+b)//2)
        ok, f = cap.read()
        if not ok:
            raise RuntimeError('failed to sample subtitle frame')
        # White caption glyphs on dark backing. Counts bright pixels.
        roi = cv2.cvtColor(f[1505:1680, 65:860], cv2.COLOR_BGR2GRAY)
        values.append(round(float((roi > 150).mean()), 5))
    cap.release()
    return values


def generate(src: Path, dst: Path, genre: str, manifest: Path):
    import cv2
    assert_review_only(genre, dst.name)
    bits, audio_duration = extract_vad(src)
    if audio_duration < 22.7:
        raise RuntimeError('audio missing or truncated')
    ratios = speech_coverage(bits)
    if any(r < .25 for r in ratios):
        raise RuntimeError('speech activity gate failed; do not publish')
    ink = video_caption_presence(src)
    if any(v < .015 for v in ink):
        raise RuntimeError('visual caption presence gate failed; do not publish')
    cap = cv2.VideoCapture(str(src))
    width, height = int(cap.get(3)), int(cap.get(4))
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (width, height, count) != (1080, 1920, 691):
        raise RuntimeError('unexpected video geometry or frame count')
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y',
           '-f','rawvideo','-vcodec','rawvideo','-pix_fmt','bgr24',
           '-s','1080x1920','-r','30','-i','pipe:0',
           '-i',str(src),'-map','0:v:0','-map','1:a:0',
           '-c:v','libx264','-preset','veryfast','-crf','19',
           '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dst)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(count):
            ok, f = cap.read()
            if not ok:
                raise RuntimeError('video decode ended early')
            draw_timeline(f, i, bits)
            p.stdin.write(f.tobytes())
    finally:
        cap.release()
        if p.stdin:
            p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError('ffmpeg encode failed')
    report = dict(cycle=922, genre=genre, status=REVIEW_STATUS,
                  source_sha256=sha256(src), output_sha256=sha256(dst),
                  scene_speech_vad_ratio=ratios, subtitle_bright_pixel_fraction=ink,
                  caption_meaning_check='NOT_DONE_NO_INDEPENDENT_JAPANESE_ASR',
                  vad_limit='VAD cannot distinguish all speech from music',
                  video_speech_visualization='replaced only original bottom progress track',
                  audio_codec='COPY_NOT_REENCODED',
                  employee_approved=False, auto_post=False)
    manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--genre', choices=GENRES, default='ai_work')
    a = p.parse_args()
    print(json.dumps(generate(a.input, a.output, a.genre, a.manifest), ensure_ascii=False))

if __name__ == '__main__':
    main()
