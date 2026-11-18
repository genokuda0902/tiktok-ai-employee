"""Lossless streaming-ready MP4 packaging for all ten genres. Requires ffmpeg."""
import argparse
import subprocess
from pathlib import Path

def package(source: Path, destination: Path):
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-y", "-i", str(source),
                    "-map", "0:v:0", "-map", "0:a:0", "-c", "copy",
                    "-movflags", "+faststart", str(destination)], check=True)
    data = destination.read_bytes()
    if not (0 <= data.find(b"moov") < data.find(b"mdat")):
        raise ValueError("Fast-start moov atom is not before mdat")
    return destination

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    package(args.source, args.destination)
