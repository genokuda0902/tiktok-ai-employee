"""Synthetic 1.5-second H264/AAC full decode; NOT private Japanese review MP4."""
import subprocess
from pathlib import Path
from pause_safe import schedule
out=Path("/tmp/cycle1052_synthetic.mp4")
def run(args):
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-2000:])
run(["ffmpeg","-hide_banner","-loglevel","error","-y",
     "-f","lavfi","-i","color=c=0x10283c:s=1080x1920:r=30:d=1.5",
     "-f","lavfi","-i","sine=frequency=440:sample_rate=48000:duration=1.5",
     "-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","ultrafast",
     "-pix_fmt","yuv420p","-c:a","aac","-shortest",str(out)])
run(["ffmpeg","-v","error","-xerror","-i",str(out),"-f","null","-"])
assert out.stat().st_size>1000
assert schedule((.9,),[(.8,1.1)],duration=1.5)[0]["status"]=="PAUSE_PLACED"
assert schedule((.9,),[],duration=1.5)[0]["status"]=="SUPPRESSED_NO_SAFE_PAUSE"
print("PASS synthetic 1.5s H264/AAC full decode; private final MP4 NOT in CI")
