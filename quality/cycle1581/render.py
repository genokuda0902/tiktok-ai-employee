import subprocess,sys
from pathlib import Path
src=Path(sys.argv[1]); dst=Path(sys.argv[2]); dst.parent.mkdir(parents=True,exist_ok=True)
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-map','0:v:0','-map','0:a:0','-map','0:s:0','-vf','deband=1thr=0.012:2thr=0.012:3thr=0.012:4thr=0.012:range=12:blur=1','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-r','30','-c:a','copy','-c:s','copy','-movflags','+faststart',str(dst)]
subprocess.run(cmd,check=True)
