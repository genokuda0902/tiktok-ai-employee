"""Offline review-only pacing repair: shared EDL trims full narration and burned-caption video.

Never posts, uploads media, calls paid services, or asserts publication approval.
"""
import argparse
import json
import math
import re
import subprocess
from pathlib import Path

FPS = 30
SCENE_FRAMES = (101, 93, 91, 99, 98, 101, 89, 103)
CUT_FRAMES = 12
GENRES = ('ai_work', 'sales_business', 'beauty', 'romance', 'saving',
          'career', 'wellness', 'science', 'travel_food', 'productivity')

def silences(path, threshold='-35dB', minimum=0.45):
    cmd = ['ffmpeg', '-hide_banner', '-i', str(path), '-af',
           f'silencedetect=noise={threshold}:d={minimum}', '-f', 'null', '-']
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-2000:])
    starts = [float(x) for x in re.findall(r'silence_start:\s*([\d.]+)', p.stderr)]
    ends = [float(x) for x in re.findall(r'silence_end:\s*([\d.]+)', p.stderr)]
    return list(zip(starts, ends))

def cuts_for_silences(gaps, frames=SCENE_FRAMES, trim_frames=CUT_FRAMES):
    cuts = []
    boundary = 0
    for count in frames[:-1]:
        boundary += count
        t = boundary / FPS
        candidates = [(a, b) for a, b in gaps if a < t < b and b-a >= 0.75]
        if len(candidates) != 1:
            raise ValueError(f'No unique safe silence at {t:.3f}s: {candidates}')
        a, b = candidates[0]
        start = math.ceil((a + 0.065) * FPS)
        end = start + trim_frames
        if end > boundary - 2 or end / FPS > b - 0.065:
            raise ValueError(f'Unsafe cut {start}:{end} in {a}:{b}')
        cuts.append((start, end))
    return cuts

def kept_ranges(cuts, total_frames=sum(SCENE_FRAMES)):
    result, last = [], 0
    for a, b in cuts:
        if a <= last or b <= a:
            raise ValueError('Overlapping or invalid cuts')
        result.append((last, a))
        last = b
    result.append((last, total_frames))
    if sum(b-a for a,b in result) != total_frames-sum(b-a for a,b in cuts):
        raise AssertionError('Frame accounting mismatch')
    return result

def render(input_mp4, narration, output_mp4, genre='ai_work'):
    if genre not in GENRES:
        raise ValueError('Unknown genre')
    cuts = cuts_for_silences(silences(narration))
    ranges = kept_ranges(cuts)
    filters = []
    for i, (a, b) in enumerate(ranges):
        filters.append(f'[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v{i}]')
        filters.append(f'[1:a]atrim=start={a/FPS:.9f}:end={b/FPS:.9f},asetpts=PTS-STARTPTS[a{i}]')
    filters.append(''.join(f'[v{i}][a{i}]' for i in range(len(ranges)))
                   + f'concat=n={len(ranges)}:v=1:a=1[v][a]')
    output_mp4 = Path(output_mp4)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
           '-filter_complex_threads', '2', '-threads', '2',
           '-i', str(input_mp4), '-i', str(narration),
           '-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '19',
           '-pix_fmt', 'yuv420p', '-r', str(FPS),
           '-c:a', 'aac', '-b:a', '160k', '-ar', '48000',
           '-movflags', '+faststart', str(output_mp4)]
    subprocess.run(cmd, check=True, timeout=240)
    return {'cuts': cuts, 'frames': sum(b-a for a,b in ranges),
            'removed_seconds': len(cuts)*CUT_FRAMES/FPS, 'genre': genre}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--audio', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--genre', default='ai_work')
    a = parser.parse_args()
    print(json.dumps(render(a.input, a.audio, a.output, a.genre)))
