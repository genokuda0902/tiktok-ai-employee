"""Mux selectable Japanese timed captions into a review-only MP4.

Captions are timed text, NOT proof of narration or speech synchronization.
"""
from pathlib import Path
import subprocess


def timestamp(seconds: float) -> str:
    if seconds < 0:
        raise ValueError("negative caption time")
    ms = round(seconds * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def make_srt(scenes: list[tuple[float, float, str]], destination: Path) -> None:
    if not scenes:
        raise ValueError("empty caption timeline")
    previous_end = 0.0
    blocks = []
    for index, (start, end, text) in enumerate(scenes, 1):
        if start < previous_end or end <= start or not text.strip():
            raise ValueError("invalid, overlapping or empty caption")
        if "\n\n" in text:
            raise ValueError("blank lines not allowed inside caption")
        blocks.append(f"{index}\n{timestamp(start)} --> {timestamp(end)}\n{text}")
        previous_end = end
    destination.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def mux_captions(video: Path, srt: Path, output: Path) -> None:
    if video.resolve() == output.resolve():
        raise ValueError("input and output must differ")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(srt),
        "-map", "0:v:0", "-map", "1:0", "-c:v", "copy",
        "-c:s", "mov_text", "-metadata:s:s:0", "language=jpn",
        "-movflags", "+faststart", str(output),
    ], check=True)


if __name__ == "__main__":
    raise SystemExit("Import make_srt/mux_captions from a reviewed renderer")
