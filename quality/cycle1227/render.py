"""Review-only reusable animated evidence checklist; not a publication pipeline."""
import argparse
import subprocess
from pathlib import Path

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def filters():
    layers = []
    for i, (label, start) in enumerate([
        ("目的を明確に", 7), ("条件を具体的に", 9), ("最後に検証", 11)
    ]):
        y = 1040 + i * 130
        enabled = f"between(t,{start},14)"
        layers.extend([
            f"drawbox=x=125:y={y}:w=830:h=108:color=0x091b35@0.94:t=fill:enable='{enabled}'",
            f"drawbox=x=125:y={y}:w=12:h=108:color=0x38bdf8:t=fill:enable='{enabled}'",
            f"drawtext=fontfile={FONT}:text='{label}':fontcolor=white:fontsize=49:x=165:y={y+24}:enable='{enabled}'",
        ])
    return ",".join(layers)

def render(source: Path, output: Path):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-i", str(source), "-vf", filters(), "-map", "0:v:0",
           "-map", "0:a?", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "copy",
           "-movflags", "+faststart", str(output)]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render(args.source, args.output)
