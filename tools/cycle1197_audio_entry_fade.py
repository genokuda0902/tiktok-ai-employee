"""Review-only audio entry fade. Reimplementation, not original v33 source."""
import argparse
import subprocess
from pathlib import Path

def build_command(source: Path, output: Path, seconds: float = 0.18) -> list[str]:
    if not 0 < seconds <= 0.5:
        raise ValueError("Fade duration must be >0 and <=0.5 seconds")
    if source.resolve() == output.resolve():
        raise ValueError("Never overwrite the input")
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(source), "-map", "0:v:0", "-map", "0:a:0",
            "-c:v", "copy", "-af", f"afade=t=in:st=0:d={seconds:g}",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
            str(output)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seconds", type=float, default=0.18)
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error("Source file does not exist")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(build_command(args.source, args.output, args.seconds), check=True)

if __name__ == "__main__":
    main()
