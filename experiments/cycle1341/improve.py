"""Review-only synthetic spreadsheet visual guidance. Does not create narration."""
from pathlib import Path
import argparse
import subprocess

def build(source: Path, output: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    vf = (
        "drawbox=x=110:y=1300:w=860:h=115:color=yellow@0.20:t=fill:enable='between(t,6,9)',"
        "drawbox=x=110:y=1285:w=860:h=145:color=yellow@0.75:t=5:enable='between(t,6,9)',"
        "drawbox=x=115:y=1300:w=850:h=115:color=green@0.22:t=fill:enable='between(t,9,12)',"
        "drawbox=x=110:y=1285:w=860:h=145:color=green@0.85:t=5:enable='between(t,9,12)',"
        "format=yuv420p"
    )
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),
                    '-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','23',
                    '-movflags','+faststart','-an',str(output)],check=True)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    build(args.source,args.output)
