#!/usr/bin/env python3
"""Offline 10-genre narration-reactive visual meter. REVIEW ONLY; no posting.

The original Japanese speech and burned captions are copied unchanged at the
encoded AAC level / left outside the meter ROI. This is not ASR.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

GENRE_COLORS = {
    'ai': (76, 226, 211), 'business': (85, 188, 255),
    'money': (244, 203, 103), 'learning': (159, 150, 251),
    'health': (87, 222, 160), 'food': (255, 170, 107),
    'travel': (104, 206, 244), 'beauty': (250, 158, 194),
    'career': (127, 196, 248), 'life': (178, 220, 138),
}
FPS = 30
METER = (704, 1457, 150, 100)
BANDS = ((120, 300), (300, 520), (520, 800), (800, 1200),
         (1200, 1900), (1900, 3100), (3100, 5700))


def run(cmd, binary=False):
    p = subprocess.run(cmd, capture_output=True, text=not binary)
    if p.returncode:
        msg = p.stderr.decode(errors='replace') if binary else p.stderr
        raise RuntimeError(f'command failed: {cmd[0]}: {msg[-1400:]}')
    return p.stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams',
                           '-show_chapters', '-show_format', '-of', 'json', str(path)]))


def audio_pcm(path, rate=16000):
    raw = run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(path),
               '-map', '0:a:0', '-ac', '1', '-ar', str(rate),
               '-f', 'f32le', '-acodec', 'pcm_f32le', 'pipe:1'], binary=True)
    return np.frombuffer(raw, dtype='<f4').copy()


def envelope(samples, frames, rate=16000, fps=FPS):
    """One amplitude + seven spectral strengths per video frame, smoothed."""
    if frames <= 0 or rate < 12000 or fps <= 0:
        raise ValueError('invalid frame/rate settings')
    win = int(.12 * rate)
    freqs = np.fft.rfftfreq(win, 1 / rate)
    rows = np.zeros((frames, 8), dtype=np.float64)
    hann = np.hanning(win)
    for i in range(frames):
        center = int((i + .5) * rate / fps)
        start = center - win // 2
        segment = np.zeros(win, dtype=np.float64)
        lo, hi = max(0, start), min(len(samples), start + win)
        if hi > lo:
            segment[lo-start:hi-start] = samples[lo:hi]
        rms = np.sqrt(np.mean(segment**2))
        db = 20 * np.log10(rms + 1e-8)
        rows[i, 0] = np.clip((db + 36) / 25, 0, 1)
        spec = np.abs(np.fft.rfft(segment * hann))
        for j, (low, high) in enumerate(BANDS):
            v = np.sqrt(np.mean(spec[(freqs >= low) & (freqs < high)]**2))
            rows[i, j+1] = np.log1p(v)
    # Per-band robust scaling; gate with actual voice amplitude.
    for j in range(1, 8):
        positive = rows[rows[:, 0] > .08, j]
        if len(positive) > 3:
            p20, p90 = np.percentile(positive, [20, 90])
            rows[:, j] = np.clip((rows[:, j] - p20) / max(p90-p20, 1e-5), 0, 1)
        else:
            rows[:, j] = 0
    levels = np.zeros((frames, 7), dtype=np.float64)
    prev = np.zeros(7, dtype=np.float64)
    for i in range(frames):
        target = rows[i, 0] * (.68 + .32 * rows[i, 1:])
        alpha = np.where(target > prev, .62, .28)  # attack/release
        prev = alpha * target + (1 - alpha) * prev
        levels[i] = np.clip(prev, 0, 1)
    return levels, rows[:, 0]


def validate_meter(width=1080, height=1920, rect=METER):
    x, y, w, h = rect
    if (width, height) != (1080, 1920) or w < 110 or h < 75:
        raise ValueError('unsupported video geometry')
    if x < 680 or y < 1430 or x+w > 880 or y+h > 1590:
        raise ValueError('meter must stay within narration widget, outside caption text')


def draw_meter(levels, genre='ai', scale=2):
    if genre not in GENRE_COLORS:
        raise ValueError('unsupported genre')
    validate_meter()
    _, _, w, h = METER
    c = GENRE_COLORS[genre]
    im = Image.new('RGBA', (w*scale, h*scale), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = lambda n: round(n*scale)
    d.rounded_rectangle((S(1), S(1), S(w-2), S(h-2)), radius=S(18),
                        fill=(4, 18, 35, 252), outline=(*c, 135), width=S(1.2))
    d.line((S(16), S(78), S(w-16), S(78)), fill=(*c, 68), width=S(1))
    for j, value in enumerate(levels):
        x = 22 + j*17
        height = 6 + round(46*float(np.clip(value, 0, 1))**1.7)
        center = 49
        y0, y1 = center - height/2, center + height/2
        # Soft halo and bright core; both are drawn only inside meter panel.
        d.rounded_rectangle((S(x-2), S(y0-2), S(x+8), S(y1+2)),
                            radius=S(5), fill=(*c, 52))
        d.rounded_rectangle((S(x), S(y0), S(x+6), S(y1)),
                            radius=S(3), fill=(*c, 255))
    return im.resize((w, h), Image.Resampling.LANCZOS)


def adts_sha(path):
    data = run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', str(path),
                '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', 'pipe:1'], binary=True)
    return hashlib.sha256(data).hexdigest()


def render(source, output, workdir, genre='ai', report=None):
    source, output, workdir = map(Path, (source, output, workdir))
    if genre not in GENRE_COLORS: raise ValueError('unsupported genre')
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError('source missing or source=output')
    validate_meter()
    info = probe(source)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    if (v['codec_name'], v['width'], v['height'], a['codec_name']) != ('h264', 1080, 1920, 'aac'):
        raise ValueError('requires H264 1080x1920 and AAC')
    frames = int(v['nb_frames'])
    samples = audio_pcm(source)
    levels, voice = envelope(samples, frames)
    frame_dir = workdir / 'meter_frames'
    frame_dir.mkdir(parents=True, exist_ok=True)
    for i, values in enumerate(levels):
        draw_meter(values, genre).save(frame_dir / f'{i:04d}.png', optimize=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    x, y, _, _ = METER
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
         '-i', str(source), '-framerate', str(FPS), '-start_number', '0',
         '-i', str(frame_dir/'%04d.png'), '-filter_complex',
         f'[0:v][1:v]overlay={x}:{y}:format=auto:shortest=0:eof_action=repeat,format=yuv420p[v]',
         '-map', '[v]', '-map', '0:a:0', '-map_chapters', '0',
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
         '-pix_fmt', 'yuv420p', '-frames:v', str(frames),
         '-c:a', 'copy', '-metadata:s:a:0', 'language=jpn',
         '-movflags', '+faststart', str(output)])
    check = probe(output)
    ov = next(s for s in check['streams'] if s['codec_type'] == 'video')
    oa = next(s for s in check['streams'] if s['codec_type'] == 'audio')
    if (ov['width'], ov['height'], int(ov['nb_frames'])) != (1080, 1920, frames):
        raise RuntimeError('video dimensions/frame count mismatch')
    if oa['codec_name'] != 'aac' or len(check['chapters']) != len(info['chapters']):
        raise RuntimeError('audio codec/chapter mismatch')
    source_audio, output_audio = adts_sha(source), adts_sha(output)
    if source_audio != output_audio: raise RuntimeError('AAC encoded packets changed')
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-xerror', '-i', str(output),
         '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'])
    chapters = []
    for c in check['chapters']:
        start, end = float(c['start_time']), float(c['end_time'])
        seg = voice[int(start*FPS):min(frames, int(end*FPS))]
        chapters.append({'start':start,'end':end,'voiced_fraction_energy_gate':
                         round(float(np.mean(seg > .15)),3) if len(seg) else None})
    data = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'output_bytes': output.stat().st_size, 'genre': genre,
            'width':1080,'height':1920,'fps':FPS,'frames':frames,
            'duration_seconds':float(check['format']['duration']),
            'chapters':chapters,'aac_adts_sha256':source_audio,
            'aac_bitstream_identical':True,'full_decode':'PASS',
            'meter_rect':list(METER), 'speech_caption_semantics':'NOT VERIFIED',
            'independent_asr':'NOT AVAILABLE',
            'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    if report:
        Path(report).parent.mkdir(parents=True, exist_ok=True)
        Path(report).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--workdir', required=True)
    p.add_argument('--genre', default='ai', choices=list(GENRE_COLORS))
    p.add_argument('--report', required=True)
    a = p.parse_args()
    print(json.dumps(render(a.source, a.output, a.workdir, a.genre, a.report), ensure_ascii=False))
