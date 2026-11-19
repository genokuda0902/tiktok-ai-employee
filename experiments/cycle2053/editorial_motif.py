"""Reusable editorial motif overlay for vertical video (Pillow + FFmpeg)."""
from PIL import Image, ImageDraw
import subprocess
from pathlib import Path

def render(source: str, destination: str):
    out = Path(destination)
    out.parent.mkdir(parents=True, exist_ok=True)
    motif = out.with_suffix(".png")
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for radius, alpha, width in [(116, 60, 3), (88, 110, 4), (56, 180, 5)]:
        d.ellipse((790-radius,370-radius,790+radius,370+radius),
                  outline=(83,235,194,alpha), width=width)
    d.ellipse((777,357,803,383), fill=(83,235,194,190))
    im.save(motif)
    subprocess.run(["ffmpeg","-y","-i",source,"-loop","1","-i",str(motif),
        "-filter_complex","[0:v][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
        "-map","[v]","-map","0:a:0","-c:v","libx264","-crf","19",
        "-c:a","copy","-movflags","+faststart",str(out)],check=True)
