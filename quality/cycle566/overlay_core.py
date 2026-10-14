"""Reusable offline 9:16 image-slide overlay. Needs ffmpeg and pre-rendered PNG."""
import argparse
import subprocess
from pathlib import Path

def overlay(source, panel, output):
    source, panel, output = map(Path, (source, panel, output))
    if not source.is_file() or not panel.is_file():
        raise FileNotFoundError('Input video or original panel PNG missing')
    output.parent.mkdir(parents=True, exist_ok=True)
    graph = (
        '[1:v]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,'
        'fade=t=out:st=1.77:d=0.15:alpha=1,setpts=PTS+2.27/TB[p];'
        '[0:v][p]overlay=60:505:eof_action=pass:repeatlast=0:format=auto,format=yuv420p[v]'
    )
    subprocess.run([
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
        '-loop', '1', '-framerate', '30', '-t', '1.92', '-i', str(panel),
        '-filter_complex', graph, '-map', '[v]', '-map', '0:a:0',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-r', '30',
        '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-t', '15.6',
        '-movflags', '+faststart', str(output)
    ], check=True)
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('panel', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    print(overlay(args.source, args.panel, args.output))
