"""Render cycle870: hybrid native slides and local Chromium interaction video.
Requires two prior-cycle MP4s in ../source. Offline, no paid API, no posting.
"""
from pathlib import Path
import subprocess, argparse
from hybrid_core import validate, overlay_filter

def render(root:Path):
    validate()
    source=root/'source'
    output=root/'output'
    output.mkdir(parents=True,exist_ok=True)
    base=source/'editorial_base_cycle869.mp4'
    demo=source/'browser_local_cycle866.mp4'
    dest=output/'cycle870_HYBRID_BROWSER_EDITORIAL_JP_HUMAN_REVIEW.mp4'
    if not base.exists() or not demo.exists():
        raise FileNotFoundError('Missing cycle869 or cycle866 source MP4')
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error',
         '-i',str(base),'-i',str(demo),'-filter_complex',overlay_filter(),
         '-map','[out]','-map','0:a:0','-frames:v','691',
         '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(dest)]
    subprocess.run(cmd,check=True)
    return dest

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',default=str(Path(__file__).resolve().parents[1]))
    args=parser.parse_args()
    print(render(Path(args.root)))
