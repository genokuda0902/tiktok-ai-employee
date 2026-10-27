"""cycle907: caption-safe, 10-genre scene wipe for authorized local MP4s.

Only transforms video pixels above the subtitle safe band. Never uploads,
merges, posts, or handles private account data. Baseline media stays local.
"""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

WIDTH, HEIGHT, FPS = 1080, 1920, 30
CONTENT_HEIGHT = 1180
CUT_FRAMES = (87, 174, 250, 348, 435, 522, 609)
WIPE_FRAMES = 8
FEATHER = 58
GENRE_COLORS = {
    'ai_work': '#24D5D0', 'business': '#53A4F8', 'education': '#F5BB51',
    'health': '#57C6A2', 'cooking': '#F3A86A', 'travel': '#6AB4EC',
    'beauty': '#DC8EBF', 'finance': '#70C6A8', 'pets': '#E1B77A',
    'entertainment': '#B39CFF',
}

def ease(t: float) -> float:
    if not 0 <= t <= 1:
        raise ValueError('progress out of range')
    return t * t * (3 - 2 * t)

def mask_for_frame(frame: int) -> np.ndarray:
    if not 0 <= frame < WIPE_FRAMES:
        raise ValueError('wipe frame out of range')
    t = ease(frame / (WIPE_FRAMES - 1))
    edge = (WIDTH + FEATHER) * (1 - t) - FEATHER * t
    x = np.arange(WIDTH, dtype=np.float32)
    alpha = np.clip((edge - x) / FEATHER, 0, 1)
    return np.uint8(np.round(alpha * 255))

def make_overlay(old_rgb: Image.Image, frame: int, genre: str) -> Image.Image:
    if genre not in GENRE_COLORS:
        raise ValueError('unapproved genre')
    if old_rgb.size != (WIDTH, HEIGHT):
        raise ValueError('expected portrait 1080x1920 source frame')
    cropped = old_rgb.convert('RGB').crop((0, 0, WIDTH, CONTENT_HEIGHT))
    rgba = cropped.convert('RGBA')
    mask = mask_for_frame(frame)
    rgba.putalpha(Image.fromarray(np.broadcast_to(mask, (CONTENT_HEIGHT, WIDTH)).copy()))
    positions = np.flatnonzero((mask > 15) & (mask < 245))
    if len(positions):
        edge_x = int(np.median(positions))
        draw = ImageDraw.Draw(rgba, 'RGBA')
        draw.rounded_rectangle(
            (max(0, edge_x-3), 30, min(WIDTH-1, edge_x+3), CONTENT_HEIGHT-30),
            radius=3, fill=GENRE_COLORS[genre] + 'B0')
    return rgba

def extract_previous_frame(video: Path, cut: int, out: Path) -> None:
    vf = f'select=eq(n\\,{cut-1})'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),
                    '-vf',vf,'-vsync','0','-frames:v','1',str(out)],check=True)
    if not out.exists():
        raise RuntimeError(f'cannot extract frame {cut-1}')

def render_overlays(video: Path, directory: Path, genre: str) -> list[Path]:
    if genre not in GENRE_COLORS:
        raise ValueError('unapproved genre')
    directory.mkdir(parents=True, exist_ok=True)
    folders = []
    for cut in CUT_FRAMES:
        folder = directory / f'cut_{cut}'
        folder.mkdir(exist_ok=True)
        frame_path = folder / 'old.png'
        extract_previous_frame(video, cut, frame_path)
        with Image.open(frame_path) as img:
            old = img.convert('RGB')
        for i in range(WIPE_FRAMES):
            make_overlay(old, i, genre).save(folder / f'frame_{i:03d}.png', compress_level=1)
        frame_path.unlink()
        folders.append(folder)
    return folders

def ffmpeg_command(video: Path, folders: list[Path], output: Path) -> list[str]:
    if len(folders) != len(CUT_FRAMES):
        raise ValueError('exactly seven cut folders required')
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video)]
    for folder in folders:
        cmd += ['-framerate',str(FPS),'-start_number','0','-i',str(folder/'frame_%03d.png')]
    filters = []
    current = '0:v'
    for idx, cut in enumerate(CUT_FRAMES, 1):
        filters.append(f'[{idx}:v]format=rgba,setpts=PTS-STARTPTS+{cut}/{FPS}/TB[o{idx}]')
        filters.append(f'[{current}][o{idx}]overlay=x=0:y=0:format=auto:repeatlast=0:eof_action=pass[v{idx}]')
        current = f'v{idx}'
    cmd += ['-filter_complex',';'.join(filters),'-map',f'[{current}]','-map','0:a:0',
            '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
            '-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(output)]
    # Keep filter graph memory bounded on hosted CI / small local machines.
    cmd[1:1] = ['-threads','2','-filter_complex_threads','1']
    return cmd

def render(video: Path, output: Path, work: Path, genre: str) -> None:
    folders = render_overlays(video, work, genre)
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(ffmpeg_command(video, folders, output), check=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--genre', choices=GENRE_COLORS, default='ai_work')
    args = parser.parse_args()
    render(args.input, args.output, args.work, args.genre)
