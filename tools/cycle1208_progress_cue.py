"""Review-only top-edge progress cue for any genre. No publication approval implied."""
import argparse
import subprocess
from pathlib import Path

def progress_filter(duration: float) -> str:
    if duration <= 0:
        raise ValueError("duration must be positive")
    return ("drawbox=x=0:y=0:w=iw:h=12:color=white@0.12:t=fill,"
            f"drawbox=x=0:y=0:w='iw*min(t/{duration:.3f}\\,1)':h=12:"
            "color=0x38bdf8@0.95:t=fill")

def render(source: Path, target: Path, duration: float) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-y","-i",str(source),
                    "-vf",progress_filter(duration),"-c:v","libx264",
                    "-preset","ultrafast","-crf","23","-pix_fmt","yuv420p",
                    "-c:a","copy","-movflags","+faststart",str(target)],check=True)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("source",type=Path)
    parser.add_argument("target",type=Path)
    parser.add_argument("--duration",type=float,required=True)
    args=parser.parse_args()
    render(args.source,args.target,args.duration)
