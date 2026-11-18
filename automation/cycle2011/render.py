"""Reusable opening hook overlay for 1080x1920 Japanese slide videos."""
import subprocess
from pathlib import Path

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def render(src: Path, dst: Path, hook: str = "最後まで見たくなる動画へ"):
    if any(c in hook for c in ":\\'%,"):
        raise ValueError("Unsupported FFmpeg drawtext punctuation")
    vf = (
        "drawbox=x=70:y=270:w=940:h=165:color=black@0.78:t=fill:"
        "enable='between(t,0,2.5)',"
        f"drawtext=fontfile={FONT}:text='{hook}':fontsize=53:fontcolor=white:"
        "x=(w-text_w)/2:y=318:enable='between(t,0,2.5)'"
    )
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src), "-vf", vf, "-c:v", "libx264",
        "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart", str(dst)
    ], check=True)
