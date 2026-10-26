"""Overlay a genuinely time-varying progress bar on a private review MP4.

Uses only FFmpeg and source MP4; audio stream is copied, never synthesized,
posted or uploaded. The genre setting affects the color only.
"""
import argparse
import json
import subprocess
from pathlib import Path
from progress_core import BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT, FPS, FRAMES, color_for_genre, validate_placement


def render(source, output, genre='ai_work'):
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    if output.exists():
        raise FileExistsError(f'refusing to overwrite: {output}')
    if not validate_placement():
        raise ValueError('unsafe progress placement')
    output.parent.mkdir(parents=True, exist_ok=True)
    duration = FRAMES / FPS
    accent = color_for_genre(genre).replace('#','0x')
    # The track clips the bar. The solid bar enters from the left so its visible
    # width increases monotonically, while captions and main image remain fixed.
    vf = (f'[1:v][2:v]overlay=x=-w+w*t/{duration:.9f}:y=0:eval=frame:shortest=1[track];'
          f'[0:v][track]overlay=x={BAR_X}:y={BAR_Y}:shortest=1:format=auto[v]')
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2',
           '-i',str(source),
           '-f','lavfi','-i',f'color=c=0x324251:s={BAR_WIDTH}x{BAR_HEIGHT}:r={FPS}:d={duration:.9f}',
           '-f','lavfi','-i',f'color=c={accent}:s={BAR_WIDTH}x{BAR_HEIGHT}:r={FPS}:d={duration:.9f}',
           '-filter_complex',vf,'-map','[v]','-map','0:a:0',
           '-frames:v',str(FRAMES),'-c:v','libx264','-preset','veryfast','-crf','18',
           '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return output

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(render(a.source,a.output,a.genre))
