"""Review-only subtitle burn-in for approved/synthetic video; never auto-publish."""
import argparse
import subprocess
from pathlib import Path

def burn(source: Path, captions: Path, output: Path) -> None:
    if not source.is_file() or not captions.is_file():
        raise FileNotFoundError("Source MP4 and caption SRT must exist")
    if source.resolve() == output.resolve():
        raise ValueError("Refuse in-place overwrite")
    output.parent.mkdir(parents=True, exist_ok=True)
    style = "FontName=Noto Sans CJK JP,FontSize=19,BorderStyle=3,BackColour=&H99000000,MarginV=150"
    # Escape characters meaningful to FFmpeg's filter parser.
    path = str(captions.resolve()).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
        "-vf",f"subtitles='{path}':force_style='{style}'",
        "-c:v","libx264","-preset","medium","-crf","22",
        "-map","0:v:0","-map","0:a?","-c:a","copy",
        "-movflags","+faststart",str(output)],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    for name in ("source","captions","output"): p.add_argument(name,type=Path)
    a=p.parse_args()
    burn(a.source,a.captions,a.output)
