"""Review-only reusable Japanese burned-caption stage. No speech claim."""
from pathlib import Path
import subprocess, argparse

def render(source: Path, captions: Path, output: Path):
    assert source.is_file() and captions.is_file()
    vf=f"subtitles={captions}:force_style='FontName=Noto Sans CJK JP,FontSize=19,PrimaryColour=&H00FFFFFF,OutlineColour=&H00121A26,BorderStyle=3,BackColour=&HBB121A26,MarginV=190,Alignment=2'"
    subprocess.run(['ffmpeg','-y','-i',str(source),'-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','23','-c:a','copy','-movflags','+faststart',str(output)],check=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--captions',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();render(a.source,a.captions,a.output)
