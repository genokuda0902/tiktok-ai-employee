"""Artwork-only shadow and detail pass. Free FFmpeg; no posting."""
import argparse
import subprocess
from pathlib import Path

ROI = (42, 378, 846, 662)
PRESETS = {
    "science": (1.12, 1.04, 1.06, .28),
    "business": (1.09, 1.04, 1.04, .24),
    "finance": (1.08, 1.05, 1.02, .26),
    "history": (1.11, 1.04, 1.04, .20),
    "travel": (1.06, 1.04, 1.08, .18),
    "food": (1.07, 1.03, 1.09, .18),
    "health": (1.08, 1.04, 1.03, .20),
    "technology": (1.12, 1.04, 1.06, .28),
    "career": (1.09, 1.04, 1.04, .24),
    "lifestyle": (1.08, 1.03, 1.05, .20),
}

def filter_graph(genre="science", roi=ROI):
    if genre not in PRESETS:
        raise ValueError("unknown genre")
    x, y, w, h = roi
    if x < 0 or y < 0 or w <= 0 or h <= 0 or x+w > 1080 or y+h > 1050:
        raise ValueError("ROI must exclude captions")
    gamma, contrast, saturation, sharpen = PRESETS[genre]
    return (f"[0:v]split=2[base][work];"
            f"[work]crop={w}:{h}:{x}:{y},"
            f"eq=gamma={gamma}:contrast={contrast}:saturation={saturation},"
            f"unsharp=5:5:{sharpen}:5:5:0[detail];"
            f"[base][detail]overlay={x}:{y}:format=auto,format=yuv420p[v]")

def render(src, dst, genre="science"):
    src, dst = Path(src), Path(dst)
    if not src.is_file() or src.resolve() == dst.resolve():
        raise ValueError("missing input or output overwrites input")
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-y", "-i", str(src),
           "-filter_complex", filter_graph(genre),
           "-map", "[v]", "-map", "0:a:0",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
           "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "copy",
           "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709", "-movflags", "+faststart", str(dst)]
    subprocess.run(cmd, check=True)
    return cmd

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--genre", choices=sorted(PRESETS), default="science")
    a = p.parse_args()
    render(a.input, a.output, a.genre)
