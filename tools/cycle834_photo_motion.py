"""Cycle834 photo-only Ken Burns effect for an existing approved-for-review MP4.

Offline FFmpeg, no uploads, no posting, no paid APIs. Inputs must be provided by
an operator with usage rights. Output remains HUMAN_REVIEW.
"""
from pathlib import Path
import subprocess

GENRE_MOTION = {
    "ai_work": (0.015, 0.18),
    "sales_business": (0.016, 0.16),
    "beauty": (0.009, 0.12),
    "romance": (0.010, 0.14),
    "saving": (0.011, 0.16),
    "career": (0.016, 0.19),
    "wellness": (0.009, 0.11),
    "science": (0.014, 0.18),
    "travel_food": (0.017, 0.20),
    "productivity": (0.014, 0.17),
}
PHOTO_RECT = (62, 390, 1018, 1390)
VIDEO_SIZE = (1080, 1920)

def motion_filter(genre="ai_work"):
    if genre not in GENRE_MOTION:
        raise ValueError("Unknown genre: " + genre)
    amplitude, travel = GENRE_MOTION[genre]
    zoom = f"1.02+{amplitude:.3f}*sin(on/38)"
    x = f"(iw-iw/zoom)*(0.5+{travel:.3f}*sin(on/45))"
    y = f"(ih-ih/zoom)*(0.5+{travel*.65:.3f}*cos(on/52))"
    return (
        f"[0:v]split[base][p];[p]crop=956:1000:62:390,"
        f"zoompan=z='{zoom}':x='{x}':y='{y}':d=1:s=956x1000:fps=30,format=rgba[pz];"
        f"[1:v]format=gray[mask];[pz][mask]alphamerge[pm];"
        f"[base][pm]overlay=62:390:shortest=1:format=auto,format=yuv420p[v]"
    )

def build_mask(destination):
    from PIL import Image, ImageDraw
    mask = Image.new("L", (956, 1000), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 955, 999), radius=34, fill=255)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    mask.save(destination)
    return destination

def render(previous_mp4, output_mp4, genre="ai_work", frames=775):
    """Render review-only MP4; never upload, merge, or publish."""
    previous_mp4, output_mp4 = Path(previous_mp4), Path(output_mp4)
    if not previous_mp4.is_file():
        raise FileNotFoundError(previous_mp4)
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    mask = build_mask(output_mp4.with_suffix(".mask.png"))
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-filter_complex_threads", "2", "-i", str(previous_mp4),
        "-loop", "1", "-framerate", "30", "-i", str(mask),
        "-filter_complex", motion_filter(genre),
        "-map", "[v]", "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "copy",
        "-frames:v", str(frames), "-movflags", "+faststart", str(output_mp4),
    ]
    subprocess.run(cmd, check=True)
    return output_mp4

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--genre", default="ai_work", choices=GENRE_MOTION)
    args = parser.parse_args()
    print(render(args.input, args.output, args.genre))
