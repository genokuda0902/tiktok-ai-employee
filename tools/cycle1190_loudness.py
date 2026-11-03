"""Review-only loudness normalization for approved local MP4s; no posting."""
import argparse
import subprocess
from pathlib import Path

TARGET_I = -16
TARGET_TP = -1.5
TARGET_LRA = 11

def command(source: str, dest: str) -> list[str]:
    if Path(source).resolve() == Path(dest).resolve():
        raise ValueError("Input and output must differ")
    return ["ffmpeg", "-y", "-i", source, "-map", "0:v:0", "-map", "0:a:0",
            "-c:v", "copy", "-af", f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
            "-movflags", "+faststart", dest]

def render(source: str, dest: str) -> None:
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(command(source, dest), check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("dest")
    args = parser.parse_args()
    render(args.source, args.dest)
