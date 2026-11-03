"""Subtle genre-neutral color grade; no external media or network dependency."""
import subprocess
from pathlib import Path

def command(source: str, output: str) -> list[str]:
    if Path(source).resolve() == Path(output).resolve():
        raise ValueError("source and output must differ")
    return ["ffmpeg","-hide_banner","-loglevel","error","-y","-i",source,
            "-vf","eq=contrast=1.025:saturation=1.035",
            "-map","0:v:0","-map","0:a?","-c:v","libx264",
            "-preset","ultrafast","-crf","22","-threads","4",
            "-c:a","copy","-movflags","+faststart",output]

def render(source: str, output: str) -> None:
    subprocess.run(command(source, output), check=True)
