"""Review-only animated comparison timer. Reimplementation, not v33 source."""
import subprocess
from pathlib import Path


def filter_expression(start=6.0, end=14.0, x=80, width=920, y=1300):
    if end <= start or width <= 0 or x < 0 or y < 0:
        raise ValueError("invalid comparison timer geometry")
    rate = width / (end - start)
    return (f"drawbox=x={x}:y={y}:w={width}:h=8:color=white@0.65:t=fill:enable='between(t,{start:g},{end:g})',"
            f"drawbox=x={x}:y={y}:w='min({width},max(0,(t-{start:g})*{rate:g}))':h=8:"
            f"color=0x38bdf8@1:t=fill:enable='between(t,{start:g},{end:g})'")


def render(source: Path, output: Path):
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError("input missing or output equals input")
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
                    "-vf", filter_expression(), "-c:v", "libx264", "-preset", "ultrafast",
                    "-crf", "24", "-c:a", "copy", "-movflags", "+faststart", str(output)], check=True)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    render(a.source, a.output)
