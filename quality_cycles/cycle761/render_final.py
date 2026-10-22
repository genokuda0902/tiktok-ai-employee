"""Cycle761: overlay two original 1080x1920 slides without losing AAC packets.

The slide images are created by render_cycle761.py and shipped in the ZIP.
This reusable muxer accepts arbitrary input duration for ten genre pipelines.
"""
import argparse
import json
import subprocess
from pathlib import Path


def run(command):
    subprocess.run(command, check=True)


def render(source, slide_a, slide_b, output, start=2.033, split=3.233, end=3.900):
    source, slide_a, slide_b, output = map(Path, (source, slide_a, slide_b, output))
    if not (0 <= start < split < end):
        raise ValueError('Invalid slide time boundaries')
    probe = subprocess.check_output([
        'ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
        '-show_entries', 'stream=nb_read_frames', '-of', 'json', str(source)
    ])
    frames = int(json.loads(probe)['streams'][0]['nb_read_frames'])
    if frames <= 0:
        raise ValueError('No video frames')
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_name('_cycle761_video_only.mp4')
    vf = (f"[0:v][1:v]overlay=0:0:enable='gte(t,{start})*lt(t,{split})'[v1];"
          f"[v1][2:v]overlay=0:0:enable='gte(t,{split})*lt(t,{end})'[v2];"
          '[v2]format=yuv420p[vout]')
    run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', str(source),
         '-loop', '1', '-i', str(slide_a), '-loop', '1', '-i', str(slide_b),
         '-filter_complex', vf, '-map', '[vout]', '-an', '-c:v', 'libx264',
         '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30',
         '-frames:v', str(frames), '-movflags', '+faststart', str(tmp)])
    try:
        run(['ffmpeg', '-hide_banner', '-y', '-loglevel', 'error', '-i', str(tmp),
             '-i', str(source), '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy',
             '-movflags', '+faststart', str(output)])
    finally:
        tmp.unlink(missing_ok=True)
    return output


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--slide-a', required=True)
    p.add_argument('--slide-b', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    print(render(a.input, a.slide_a, a.slide_b, a.output))
