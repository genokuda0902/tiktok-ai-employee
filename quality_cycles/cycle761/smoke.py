"""Synthetic MP4 smoke test for cycle761; does not validate Japanese voice."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
from render_final import render


def call(args):
    subprocess.run(args, check=True)


def audio(path):
    return hashlib.sha256(subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
        '-c', 'copy', '-f', 'adts', '-'
    ])).hexdigest()


with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp)
    for name, color in [('a', 'teal'), ('b', 'navy')]:
        call(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
              'color=c=' + color + ':s=1080x1920', '-frames:v', '1',
              '-threads', '1', str(d / (name + '.png'))])
    source = d / 'input.mp4'
    output = d / 'output.mp4'
    call(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
          'color=c=black:s=1080x1920:r=30:d=4', '-f', 'lavfi', '-i',
          'sine=frequency=440:sample_rate=48000:duration=4',
          '-c:v', 'libx264', '-preset', 'ultrafast', '-c:a', 'aac',
          '-t', '4', str(source)])
    render(source, d / 'a.png', d / 'b.png', output)
    call(['ffmpeg', '-v', 'error', '-xerror', '-i', str(output),
          '-f', 'null', '-'])
    info = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'json', str(output)
    ]))
    assert info['streams'][0]['width'] == 1080
    assert info['streams'][0]['height'] == 1920
    assert audio(source) == audio(output)
    print('PASS: synthetic 1080x1920 MP4, video decode and identical AAC packets')
