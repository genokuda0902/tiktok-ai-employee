import subprocess
from pathlib import Path

def render(source: Path, output: Path):
    """Apply conservative slide tonal adjustment; preserve AAC narration packets."""
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
        "-vf","eq=contrast=1.025:saturation=1.02:brightness=0",
        "-c:v","libx264","-preset","veryfast","-crf","19",
        "-pix_fmt","yuv420p","-r","30","-c:a","copy",
        "-movflags","+faststart",str(output)],check=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv)!=3:
        raise SystemExit("Usage: python render.py input.mp4 output.mp4")
    render(Path(sys.argv[1]),Path(sys.argv[2]))
