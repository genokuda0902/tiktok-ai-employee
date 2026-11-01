#!/usr/bin/env python3
"""Offline, original non-musical UI cues for private-review Japanese videos.

No external sound files, models, subscriptions or public posting. Source MP4 and
private manifest must stay outside the public repository.
"""
import argparse
import hashlib
import json
import math
import re
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = ('ai', 'business', 'money', 'learning', 'health', 'food', 'travel', 'beauty', 'career', 'life')
EVENT_TYPES = ('tap', 'confirm', 'reuse')
SR = 48000


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, check=False)
    if p.returncode:
        raise RuntimeError(p.stderr.decode('utf-8', 'replace')[-1600:])
    return p.stdout


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def probe(path):
    d = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    v = [s for s in d['streams'] if s['codec_type'] == 'video']
    a = [s for s in d['streams'] if s['codec_type'] == 'audio']
    s = [s for s in d['streams'] if s['codec_type'] == 'subtitle']
    if len(v) != 1 or len(a) != 1 or s:
        raise ValueError('one video, one audio and no soft subtitles required')
    if v[0]['codec_name'] != 'h264' or a[0]['codec_name'] != 'aac' or a[0]['sample_rate'] != '48000':
        raise ValueError('H264 and AAC 48kHz required')
    if v[0]['width'] * 16 != v[0]['height'] * 9 or v[0]['avg_frame_rate'] != '30/1':
        raise ValueError('9:16 portrait 30fps required')
    if a[0].get('tags', {}).get('language') != 'jpn':
        raise ValueError('Japanese narration language tag required')
    return {'width': v[0]['width'], 'height': v[0]['height'], 'frames': int(v[0]['nb_frames']),
            'duration': float(d['format']['duration'])}


def validate_manifest(m, source_sha, duration):
    if set(m) != {'policy', 'asset_approval', 'source_sha256', 'genre', 'events'}:
        raise ValueError('invalid manifest keys')
    if m['policy'] != POLICY or m['asset_approval'] != 'private_review_only' or m['source_sha256'] != source_sha:
        raise ValueError('unapproved or mismatched source')
    if m['genre'] not in GENRES:
        raise ValueError('unsupported genre')
    events = m['events']
    if not isinstance(events, list) or not 1 <= len(events) <= 5:
        raise ValueError('one to five original cues required')
    last = -1.0
    for e in events:
        if not isinstance(e, dict) or set(e) != {'time', 'type'} or e['type'] not in EVENT_TYPES:
            raise ValueError('invalid cue')
        t = e['time']
        if type(t) not in (int, float) or not math.isfinite(t) or not 0.15 <= t < duration - 0.45:
            raise ValueError('cue outside safe duration')
        if t - last < 0.45:
            raise ValueError('overlapping cues')
        last = t
    return events


def cue(kind):
    """Original, quiet UI clicks/chimes (no melody, no third-party audio)."""
    dur = {'tap': 0.12, 'confirm': 0.29, 'reuse': 0.20}[kind]
    t = np.arange(round(dur * SR), dtype=np.float64) / SR
    if kind == 'tap':
        wave = (np.sin(2 * np.pi * (670 * t + 180 * t * t)) * np.exp(-32 * t)
                + 0.18 * np.sin(2 * np.pi * 1540 * t) * np.exp(-58 * t))
    elif kind == 'confirm':
        wave = (0.75 * np.sin(2 * np.pi * 790 * t) + 0.23 * np.sin(2 * np.pi * 1185 * t)) * np.exp(-11 * t)
    else:
        wave = (0.75 * np.sin(2 * np.pi * 620 * t) + 0.2 * np.sin(2 * np.pi * 930 * t)) * np.exp(-18 * t)
    fade = np.minimum(1.0, t / 0.006)
    wave *= fade
    wave *= 0.039 / max(float(np.max(np.abs(wave))), 1e-9)  # <= -28.2 dBFS
    return wave


def make_sfx_wav(events, duration, path):
    samples = int(math.ceil(duration * SR))
    mono = np.zeros(samples, dtype=np.float64)
    for e in events:
        x = cue(e['type'])
        i = round(e['time'] * SR)
        mono[i:i + len(x)] += x[:max(0, samples - i)]
    peak = float(np.max(np.abs(mono)))
    if peak > 0.041:
        raise ValueError('effect peak unsafe')
    pcm = np.rint(np.clip(mono, -1, 1) * 32767).astype('<i2')
    with wave.open(str(path), 'wb') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())
    return peak


def video_stream_hash(path):
    return hashlib.sha256(run(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0', '-c', 'copy', '-f', 'h264', '-'])).hexdigest()


def render(source, output, manifest, report):
    source, output, manifest, report = [Path(x).resolve() for x in (source, output, manifest, report)]
    if len({source, output, manifest, report}) != 4 or output.exists() or report.exists():
        raise ValueError('unsafe overwrite')
    info = probe(source)
    m = json.loads(manifest.read_text(encoding='utf-8'))
    events = validate_manifest(m, sha256(source), info['duration'])
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='private_original_ui_sfx_') as td:
        wav = Path(td) / 'original_sfx.wav'
        effect_peak = make_sfx_wav(events, info['duration'], wav)
        run(['ffmpeg', '-hide_banner', '-v', 'error', '-nostdin', '-n', '-i', str(source), '-i', str(wav),
             '-filter_complex', '[0:a:0][1:a:0]amix=inputs=2:duration=first:normalize=0:dropout_transition=0[a]',
             '-map', '0:v:0', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
             '-ar', str(SR), '-ac', '2', '-metadata:s:a:0', 'language=jpn',
             '-movflags', '+faststart', str(output)])
    out = probe(output)
    if info['frames'] != out['frames'] or (info['width'], info['height']) != (out['width'], out['height']):
        raise AssertionError('video geometry changed')
    if abs(info['duration'] - out['duration']) > 0.05:
        raise AssertionError('duration changed')
    if video_stream_hash(source) != video_stream_hash(output):
        raise AssertionError('video stream was modified')
    run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(output), '-map', '0:v:0', '-f', 'null', '-',
         '-map', '0:a:0', '-f', 'null', '-'])
    volume = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(output), '-vn', '-af', 'volumedetect', '-f', 'null', '-'],
                            capture_output=True, text=True, check=True).stderr
    peak = float(re.search(r'max_volume:\s*(-?\d+(?:\.\d+)?) dB', volume).group(1))
    if peak > -1.0:
        raise AssertionError('audio clipping risk')
    qa = {'policy': POLICY, 'source_sha256': sha256(source), 'output_sha256': sha256(output),
          'resolution': [out['width'], out['height']], 'frames': out['frames'], 'duration': out['duration'],
          'events': events, 'original_sfx_peak': effect_peak, 'output_audio_peak_dbfs': peak,
          'video_bitstream_identical': True, 'full_av_decode': 'PASS',
          'narration_reencoded_not_bit_identical': True, 'independent_japanese_asr': 'NOT_VERIFIED',
          'caption_semantics': 'NOT_VERIFIED', 'phone_playback': 'NOT_VERIFIED',
          'asset_rights': 'NOT_VERIFIED', 'employee_approval': 'NOT_VERIFIED'}
    report.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    return qa


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for k in ('source', 'output', 'manifest', 'report'):
        p.add_argument('--' + k, required=True)
    args = p.parse_args()
    print(json.dumps(render(args.source, args.output, args.manifest, args.report), ensure_ascii=False))
