"""Optional speech rumble reduction for review videos; no automatic publication."""
import argparse
import subprocess

def render(source, output):
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", source,
        "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
        "-af", "highpass=f=75", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", output], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()
    render(args.source, args.output)
