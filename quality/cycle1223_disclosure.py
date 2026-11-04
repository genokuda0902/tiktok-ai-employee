"""Review-only disclosure overlay for conceptual demonstrations (10-genre reusable)."""
import subprocess
from pathlib import Path
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def filtergraph(start=6.0, end=14.0):
    if not 0 <= start < end:
        raise ValueError("invalid cue window")
    return (
        f"drawbox=x=105:y=1495:w=870:h=108:color=black@0.82:t=fill:enable='between(t,{start},{end})',"
        f"drawtext=fontfile={FONT}:text='※ 実際の操作映像ではありません':fontsize=39:fontcolor=white:"
        f"x=(w-text_w)/2:y=1528:enable='between(t,{start},{end})'"
    )

def render(src: Path, dst: Path):
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
        "-vf", filtergraph(), "-map", "0:v:0", "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(dst)
    ], check=True)
