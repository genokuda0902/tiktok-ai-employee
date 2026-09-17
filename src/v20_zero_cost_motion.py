#!/usr/bin/env python3
"""Render v20 visuals with narration-aligned subtitles, fail closed on missing data."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / 'assets/v20/storyboard.jpg'
OUT = ROOT / 'output/v20_motion'
OUT.mkdir(parents=True, exist_ok=True)
SCENES = OUT / 'scenes'
SCENES.mkdir(exist_ok=True)
if not STORY.is_file():
    raise SystemExit('Missing storyboard')
W, H = 600, 1066
for i, (r, c) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)], 1):
    x, y, w, h = c * (W // 2), r * (H // 3), W // 2, H // 3
    subprocess.run(['convert', str(STORY), '-crop', f'{w}x{h}+{x}+{y}', '+repage', '-resize', '1080x1920^', '-gravity', 'center', '-extent', '1080x1920', str(SCENES / f's{i}.jpg')], check=True)
durs = [4, 4, 5, 5, 6, 8]
clips = []
for i, d in enumerate(durs, 1):
    frames = d * 30
    src, dst = SCENES / f's{i}.jpg', OUT / f'clip_{i}.mp4'
    if i % 2:
        move = f"zoompan=z='min(zoom+0.0015,1.14)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"
    else:
        move = f"zoompan=z=1.12:x='min((iw-iw/zoom)*on/{frames},iw-iw/zoom)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"
    vf = 'scale=1200:2134:force_original_aspect_ratio=increase,crop=1200:2134,' + move + ',format=yuv420p'
    subprocess.run(['ffmpeg', '-y', '-loop', '1', '-i', str(src), '-vf', vf, '-t', str(d), '-r', '30', '-an', '-c:v', 'libx264', '-crf', '18', str(dst)], check=True)
    clips.append(dst)
(OUT / 'concat.txt').write_text(''.join(f"file '{p.name}'\n" for p in clips), encoding='utf-8')
visual = OUT / 'visual.mp4'
subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', 'visual.mp4'], cwd=OUT, check=True)
voice = ROOT / 'output/narration.wav'
timings_file = ROOT / 'output/narration_timing.json'
if not voice.is_file() or not timings_file.is_file():
    raise SystemExit('Missing narration or narration timings')
timings = json.loads(timings_file.read_text(encoding='utf-8'))
if not timings or any(not item.get('text') or float(item['end']) <= float(item['start']) for item in timings):
    raise SystemExit('Invalid narration timings')

def stamp(seconds):
    milliseconds = round(float(seconds) * 1000)
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    secs, millis = divmod(remainder, 1000)
    return f'{hours:02}:{minutes:02}:{secs:02},{millis:03}'

srt = OUT / 'captions.srt'
srt.write_text(''.join(f"{i}\n{stamp(item['start'])} --> {stamp(item['end'])}\n{item['text']}\n\n" for i, item in enumerate(timings, 1)), encoding='utf-8')
final = OUT / 'AI時短ラボ_01_v20_final.mp4'
style = 'FontName=Noto Sans CJK JP,FontSize=18,Alignment=2,MarginV=180,Outline=3,Shadow=1'
subprocess.run(['ffmpeg', '-y', '-i', str(visual), '-i', str(voice), '-vf', f"subtitles={srt}:force_style='{style}'", '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-shortest', str(final)], check=True)
probe = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height,codec_name', '-show_entries', 'format=duration,size', '-of', 'json', str(final)], text=True)
(OUT / 'report.json').write_text(probe, encoding='utf-8')
print(final)
