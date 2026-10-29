"""Cycle952: three-step, non-destructive mobile reading guide for a fictional prompt editor.

No image generation, downloads, or publishing. Requires an explicitly authorized local MP4.
Only ai_work geometry has been visually checked; other genres need their own geometry.
"""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 1920, 30
GENRE_COLORS = {
    "ai_work": "#29E3CD", "business": "#F4BA68", "finance": "#7DD3FC",
    "education": "#A5B4FC", "technology": "#67E8F9", "health": "#86EFAC",
    "travel": "#F9A8D4", "food": "#FDBA74", "lifestyle": "#C4B5FD",
    "entertainment": "#FCA5A5",
}
EDITOR_SAFE = (125, 535, 920, 1090)
CAPTION_ZONE = (30, 1240, 930, 1455)
HEADER_ZONE = (0, 0, 1080, 350)
FOOTER_ZONE = (0, 1460, 1080, 1920)
PHASES = (
    {"label": "目的", "index": 1, "start": 8.94, "end": 9.72, "rect": (171, 690, 886, 801)},
    {"label": "条件", "index": 2, "start": 9.74, "end": 10.54, "rect": (171, 820, 886, 936)},
    {"label": "形式", "index": 3, "start": 10.56, "end": 11.38, "rect": (171, 951, 886, 1066)},
)
FONT_CANDIDATES = (
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)

def intersects(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]

def validate(genre, width=WIDTH, height=HEIGHT, fps=FPS):
    if genre not in GENRE_COLORS:
        raise ValueError(f"unknown genre: {genre}")
    if (width, height, fps) != (WIDTH, HEIGHT, FPS):
        raise ValueError("geometry validated only for 1080x1920 @30fps")
    if genre != "ai_work":
        raise ValueError("fail closed: only ai_work has approved editor coordinates")
    for p in PHASES:
        x1, y1, x2, y2 = p["rect"]
        assert EDITOR_SAFE[0] <= x1 < x2 <= EDITOR_SAFE[2]
        assert EDITOR_SAFE[1] <= y1 < y2 <= EDITOR_SAFE[3]
        assert not any(intersects(p["rect"], protected) for protected in (CAPTION_ZONE, HEADER_ZONE, FOOTER_ZONE))
        assert 8.7 < p["start"] < p["end"] < 11.6
    for a, b in zip(PHASES, PHASES[1:]):
        assert a["end"] < b["start"]
    return True

def font(size):
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def render_overlay(phase, out, color=GENRE_COLORS["ai_work"]):
    im = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    x1, y1, x2, y2 = phase["rect"]
    rgb = tuple(bytes.fromhex(color.lstrip("#")))
    d.rounded_rectangle((x1-5, y1-5, x2+5, y2+5), radius=20, outline=rgb+(70,), width=12)
    d.rounded_rectangle((x1, y1, x2, y2), radius=16, outline=rgb+(245,), width=5)
    d.rectangle((x1-9, y1+22, x1-3, y2-22), fill=rgb+(240,))
    d.rounded_rectangle((147, 544, 385, 588), radius=13, fill=(2, 22, 35, 224), outline=rgb+(210,), width=2)
    d.text((161, 547), f'いま：{phase["label"]}', font=font(25), fill=(255,255,255,255))
    im.save(out)
    return out

def make_filter(phases=PHASES):
    filters = []
    last = "0:v"
    for i, p in enumerate(phases, 1):
        fadein = p["start"]
        fadeout = p["end"] - 0.14
        filters.append(f"[{i}:v]format=rgba,fade=t=in:st={fadein:.2f}:d=0.14:alpha=1,fade=t=out:st={fadeout:.2f}:d=0.14:alpha=1[focus{i}]")
        nxt = f"base{i}"
        filters.append(f"[{last}][focus{i}]overlay=0:0:format=auto:shortest=1:eof_action=pass:enable='between(t,{p['start']:.2f},{p['end']:.2f})'[{nxt}]")
        last = nxt
    return ";".join(filters), last

def build_cmd(source, overlays, video_only, crf=18):
    fc, last = make_filter()
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source)]
    for overlay in overlays:
        cmd += ["-loop", "1", "-framerate", str(FPS), "-i", str(overlay)]
    cmd += ["-filter_complex", fc, "-map", f"[{last}]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", "-r", str(FPS), "-frames:v", "691", "-movflags", "+faststart", str(video_only)]
    return cmd

def run(source, output, workdir, genre):
    validate(genre)
    source, output, workdir = Path(source), Path(output), Path(workdir)
    if not source.is_file():
        raise FileNotFoundError(source)
    workdir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    overlays = [render_overlay(p, workdir / f"focus_{i}.png") for i, p in enumerate(PHASES, 1)]
    intermediate = workdir / "video_only.mp4"
    subprocess.run(build_cmd(source, overlays, intermediate), check=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(intermediate), "-i", str(source), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", str(output)], check=True)
    return output

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--genre", default="ai_work")
    args = ap.parse_args()
    print(run(args.input, args.output, args.workdir, args.genre))
