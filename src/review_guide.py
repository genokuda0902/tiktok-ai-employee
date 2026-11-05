"""Review-only safe-zone callouts; reimplementation, not v33 source."""
from pathlib import Path
import subprocess

def review_filter(font: str) -> str:
    if not font or not Path(font).is_file():
        raise ValueError("Existing Japanese font required")
    lines = [
        (4, 8, "映像・音声・字幕を確認"),
        (13, 17, "公開前に人が最終確認"),
    ]
    parts = []
    for start, end, message in lines:
        gate = f"between(t,{start},{end})"
        parts.append(f"drawbox=x=100:y=400:w=880:h=170:color=black@0.75:t=fill:enable='{gate}'")
        parts.append(f"drawtext=fontfile={font}:text='{message}':fontcolor=white:fontsize=47:x=(w-text_w)/2:y=455:enable='{gate}'")
    return ",".join(parts)

def render(source: Path, output: Path, font: str) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(source), "-vf", review_filter(font),
                    "-map", "0:v:0", "-map", "0:a?", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags",
                    "+faststart", str(output)], check=True)
