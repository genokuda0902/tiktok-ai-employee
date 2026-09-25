"""Zero-cost narration mastering for image-slide videos.

Keeps video untouched and applies conservative speech cleanup + EBU-style loudness
normalization. This module does not publish or upload media.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


def build_filter() -> str:
    return "highpass=f=80,lowpass=f=14500,loudnorm=I=-16:LRA=7:TP=-1.5"


def build_command(src: str, dst: str) -> list[str]:
    if not src.lower().endswith(".mp4") or not dst.lower().endswith(".mp4"):
        raise ValueError("src and dst must be MP4 files")
    return [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", src,
        "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
        "-af", build_filter(), "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-ac", "2", "-movflags", "+faststart", dst,
    ]


def master(src: str, dst: str) -> None:
    if Path(src).resolve() == Path(dst).resolve():
        raise ValueError("refuse in-place overwrite")
    subprocess.run(build_command(src, dst), check=True)
