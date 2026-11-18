"""Review-only reusable action pointer. Requires approved input video."""
from pathlib import Path
import subprocess
import sys

def build(source: Path, output: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    vf = ("drawbox=x='200+240*min(t/4,1)':y='630+190*min(t/4,1)':w=105:h=105:"
          "color=yellow@0.20:t=fill:enable='between(t,2,6)',"
          "drawbox=x='200+240*min(t/4,1)':y='630+190*min(t/4,1)':w=105:h=105:"
          "color=yellow@0.9:t=5:enable='between(t,2,6)'")
    cmd = ['ffmpeg','-y','-v','error','-i',str(source),'-vf',vf,
           '-map','0:v:0','-map','0:a?','-map','0:s?',
           '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',
           '-c:a','copy','-c:s','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return output

if __name__ == '__main__':
    build(Path(sys.argv[1]),Path(sys.argv[2]))
