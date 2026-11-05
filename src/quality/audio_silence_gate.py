"""Fail-closed silence interval detector for review-only TikTok renders."""
import re
import subprocess
from pathlib import Path
START = re.compile(r'silence_start:\s*([0-9.]+)')
END = re.compile(r'silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)')
def parse_silence(log: str):
    intervals = []
    start = None
    for line in log.splitlines():
        a = START.search(line)
        b = END.search(line)
        if a:
            start = float(a.group(1))
        if b and start is not None:
            intervals.append((start, float(b.group(1)), float(b.group(2))))
            start = None
    return intervals
def inspect(path: str, threshold_db=-35, minimum_seconds=0.5):
    if not Path(path).is_file():
        raise FileNotFoundError(path)
    cmd = ['ffmpeg','-hide_banner','-i',path,'-vn','-af',
           f'silencedetect=noise={threshold_db}dB:d={minimum_seconds}', '-f','null','-']
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-1200:])
    return parse_silence(result.stderr)
