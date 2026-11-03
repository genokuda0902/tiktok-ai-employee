"""Cycle1184: non-invasive top progress rail for 9:16 review videos.

Reimplementation, not original v33. No private assets are bundled.
"""
import argparse
import subprocess

DURATION = 23.033333
def progress_filter(duration: float) -> str:
    if duration <= 0:
        raise ValueError("duration must be positive")
    return ("drawbox=x=0:y=0:w=iw:h=12:color=black@0.45:t=fill,"
            "drawbox=x=0:y=0:w='min(iw,iw*t/" + f"{duration:.6f}" +
            ")':h=12:color=white@0.9:t=fill")

def render(source: str, output: str, duration: float = DURATION) -> None:
    subprocess.run(["ffmpeg", "-y", "-i", source, "-vf", progress_filter(duration),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                    "-c:a", "copy", "-movflags", "+faststart", output], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()
    render(args.source, args.output)
