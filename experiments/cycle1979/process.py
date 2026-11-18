import subprocess,sys
from pathlib import Path
src=Path(sys.argv[1]); out=Path(sys.argv[2])
subprocess.run(['ffmpeg','-y','-i',str(src),'-vf','drawbox=x=40:y=1538:w=1000:h=3:color=white@0.42:t=fill','-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(out)],check=True)
