"""Review-only 1080x1920 FFmpeg export of an existing original synthetic MP4."""
import subprocess
from pathlib import Path

FILTER = "fps=24,scale=1080:1920:flags=lanczos,format=yuv420p"
def render(source: Path, output: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-vf",FILTER,"-c:v","libx264","-preset","veryfast","-crf","20","-c:a","aac","-b:a","128k","-movflags","+faststart",str(output)],check=True)
    return output
if __name__ == "__main__":
    import sys
    if len(sys.argv)!=3: raise SystemExit("usage: python review_export.py input.mp4 output.mp4")
    render(Path(sys.argv[1]),Path(sys.argv[2]))
