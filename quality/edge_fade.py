"""Reusable subtle edge fade for vertical TikTok slides."""
import subprocess

def fade_filter(duration: float, fade: float = 0.22) -> str:
    if duration <= 2 * fade or not 0.05 <= fade <= 0.6:
        raise ValueError("invalid duration or fade")
    return f"fade=t=in:st=0:d={fade},fade=t=out:st={duration-fade:.3f}:d={fade}"

def render(source: str, output: str, duration: float):
    subprocess.run(["ffmpeg", "-y", "-i", source, "-vf", fade_filter(duration), "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", output], check=True)
