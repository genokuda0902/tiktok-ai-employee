#!/usr/bin/env python3
"""Decode the entire fixture with bundled FFmpeg, check streams and dimensions."""
import argparse,subprocess
from pathlib import Path
import imageio_ffmpeg

def verify(path):
    path=Path(path)
    if not path.exists():raise FileNotFoundError(path)
    exe=imageio_ffmpeg.get_ffmpeg_exe()
    probe=subprocess.run([exe,'-hide_banner','-i',str(path)],capture_output=True,text=True)
    info=probe.stderr
    assert 'Video: h264' in info,info[-1500:]
    assert 'Audio: aac' in info,info[-1500:]
    assert '1080x1920' in info,info[-1500:]
    subprocess.run([exe,'-v','error','-xerror','-i',str(path),'-f','null','-'],check=True)
    print('PASS: 1080x1920 H.264/AAC full decode; synthetic tone is NOT Japanese narration')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--path',required=True)
    verify(ap.parse_args().path)
