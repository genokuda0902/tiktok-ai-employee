"""Cycle489 review-only MP4 compositor. Requires a locally approved review source."""
import argparse, subprocess
from pathlib import Path
from hook_art import frames
def run(cmd):
    subprocess.run(cmd,check=True)
def build(source,out):
    source=Path(source);out=Path(out)
    if not source.is_file():raise FileNotFoundError(source)
    out.parent.mkdir(parents=True,exist_ok=True)
    folder=frames(out.parent/'hook_frames')
    intro=out.parent/'hook.mp4'
    run(['ffmpeg','-y','-v','error','-framerate','30','-i',str(folder/'%03d.png'),'-c:v','libx264','-pix_fmt','yuv420p',str(intro)])
    filt='[0:v]setpts=PTS-STARTPTS[a];[1:v]trim=start=1.5,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0,fps=30[v]'
    run(['ffmpeg','-y','-v','error','-i',str(intro),'-i',str(source),'-filter_complex',filt,'-map','[v]','-map','1:a:0','-c:v','libx264','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(out)])
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--out',required=True)
    a=p.parse_args()
    print(build(a.source,a.out))
