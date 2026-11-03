"""Review-only subtitle contrast backdrop; input must be an approved, locally available MP4."""
import argparse
import subprocess
from pathlib import Path

def command(source: str, output: str, alpha: float = 0.16) -> list[str]:
    if not 0 <= alpha <= 0.3:
        raise ValueError("alpha must be between 0 and 0.3")
    if Path(source).resolve() == Path(output).resolve():
        raise ValueError("input and output must differ")
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", source,
            "-vf", f"drawbox=x=0:y=ih*0.755:w=iw:h=ih*0.245:color=black@{alpha}:t=fill",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-c:a", "copy", "-movflags", "+faststart", output]

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("output")
    p.add_argument("--alpha", type=float, default=0.16)
    a = p.parse_args()
    subprocess.run(command(a.source, a.output, a.alpha), check=True)
