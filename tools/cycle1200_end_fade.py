"""Review-only ending fade for already approved-to-process local MP4s.

Never uploads inputs or outputs. Does not grant publication permission.
"""
import argparse
import subprocess


def fade_start(duration: float, fade_seconds: float = 0.45) -> float:
    if duration <= 0 or fade_seconds <= 0 or fade_seconds >= duration:
        raise ValueError("fade must be positive and shorter than duration")
    return round(duration - fade_seconds, 3)


def command(source: str, destination: str, duration: float, fade_seconds: float = 0.45) -> list[str]:
    if source == destination:
        raise ValueError("refuse to overwrite source")
    start = fade_start(duration, fade_seconds)
    return ["ffmpeg", "-hide_banner", "-y", "-i", source,
            "-vf", f"fade=t=out:st={start}:d={fade_seconds}",
            "-af", f"afade=t=out:st={start}:d={fade_seconds}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", destination]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("destination")
    p.add_argument("--duration", type=float, required=True)
    args = p.parse_args()
    subprocess.run(command(args.source, args.destination, args.duration), check=True)


if __name__ == "__main__":
    main()
