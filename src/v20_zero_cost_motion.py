#!/usr/bin/env python3
"""Render v20 storyboard with narration-timed captions and no truncated audio."""
import json
import math
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / 'assets/v20/storyboard.jpg'
OUT = ROOT / 'output/v20_motion'
SCENES = OUT / 'scenes'
VOICE = ROOT / 'output/narration.wav'
TIMINGS = ROOT / 'output/narration_timing.json'
if not STORY.is_file() or not VOICE.is_file() or not TIMINGS.is_file():
    raise SystemExit('Missing storyboard, narration or narration timings')
with wave.open(str(VOICE), 'rb') as wav:
    voice_seconds = wav.getnframes() / wav.getframerate()
timings = json.loads(TIMINGS.read_text(encoding='utf-8'))
if not isinstance(timings, list) or not timings:
    raise SystemExit('Missing narration timing entries')
previous_end = 0.0
for item in timings:
    if not isinstance(item, dict) or not item.get('text'):
        raise SystemExit('Invalid subtitle text')
    start, end = float(item['start']), float(item['end'])
    if start < previous_end - 0.01 or end <= start or end > voice_seconds + 0.1:
        raise SystemExit('Subtitle timing does not match narration')
    previous_end = end
if not 20 <= voice_seconds <= 45:
    raise SystemExit(f'Narration duration {voice_seconds:.2f}s is outside 20-45s')
OUT.mkdir(parents=True, exist_ok=True)
SCENES.mkdir(parents=True, exist_ok=True)
W, H = 600, 1066
for i, (r, c) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)], 1):
    x, y, w, h = c * (W // 2), r * (H // 3), W // 2, H // 3
    subprocess.run(['convert', str(STORY), '-crop', f'{w}x{h}+{x}+{y}', '+repage', '-resize', '1080x1920^', '-gravity', 'center', '-extent', '1080x1920', str(SCENES / f's{i}.jpg')], check=True)
# Give visuals enough frames to cover the entire generated narration; never cut off speech.
weights = [4, 4, 5, 5, 6, 8]
total_frames = math.ceil((voice_seconds + 0.15) * 30)
frames_per_scene = [max(1, round(total_frames * weight / sum(weights))) for weight in weights[:-1]]
frames_per_scene.append(total_frames - sum(frames_per_scene))
if frames_per_scene[-1] <= 0:
    raise SystemExit('Invalid scene duration allocation')
clips = []
for i, frames in enumerate(frames_per_scene, 1):
    duration = frames / 30
    src, dst = SCENES / f's{i}.jpg', OUT / f'clip_{i}.mp4'
    if i % 2:
        move = f"zoompan=z='min(zoom+0.0015,1.14)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"
    else:
        move = f"zoompan=z=1.12:x='min((iw-iw/zoom)*on/{frames},iw-iw/zoom)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30"
    vf = 'scale=1200:2134:force_original_aspect_ratio=increase,crop=1200:2134,' + move + ',format=yuv420p'
    subprocess.run(['ffmpeg', '-y', '-loop', '1', '-i', str(src), '-vf', vf, '-frames:v', str(frames), '-r', '30', '-an', '-c:v', 'libx264', '-crf', '18', str(dst)], check=True)
    clips.append(dst)
(OUT / 'concat.txt').write_text(''.join(f"file '{p.name}'\n" for p in clips), encoding='utf-8')
visual = OUT / 'visual.mp4'
subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy', 'visual.mp4'], cwd=OUT, check=True)

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
subprocess.run(['ffmpeg', '-y', '-i', str(visual), '-i', str(VOICE), '-vf', f"subtitles={srt}:force_style='{style}'", '-c:v', 'libx264', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-shortest', str(final)], check=True)
probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height,codec_name', '-show_entries', 'format=duration,size', '-of', 'json', str(final)], text=True))
actual_duration = float(probe['format']['duration'])
if actual_duration < voice_seconds - 0.15:
    final.unlink(missing_ok=True)
    raise SystemExit(f'Final video truncated narration: video={actual_duration:.2f}s voice={voice_seconds:.2f}s')
(OUT / 'report.json').write_text(json.dumps({'probe': probe, 'narration_seconds': voice_seconds, 'subtitles': len(timings)}, ensure_ascii=False, indent=2), encoding='utf-8')
print(final)
