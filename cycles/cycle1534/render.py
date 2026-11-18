"""Cycle1534: reusable time-progress overlay; preserves existing subtitle stream."""
from pathlib import Path
import subprocess, json, sys
ROOT=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'source.mp4'
out=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'cycle1534_REVIEW_ONLY.mp4'
if not source.exists(): raise FileNotFoundError(source)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(source)]))
duration=float(probe['format']['duration'])
if duration<=0: raise ValueError('invalid duration')
vf=f"drawbox=x=42:y=1132:w=636:h=8:color=white@0.20:t=fill,drawbox=x=42:y=1132:w='min(636,636*t/{duration})':h=8:color=0x38bdf8@0.95:t=fill"
cmd=['ffmpeg','-y','-v','error','-i',str(source),'-filter_complex',f'[0:v]{vf}[v]','-map','[v]','-map','0:a?','-map','0:s?','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-c:a','copy','-c:s','copy','-movflags','+faststart',str(out)]
subprocess.run(cmd,check=True)
print(out)
