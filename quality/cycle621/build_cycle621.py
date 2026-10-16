#!/usr/bin/env python3
"""Cycle 621: remove ghosted intra-chapter crossfade using a top-down pixel-mask wipe.
Original media is private; this module does not publish or upload.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets/cycle620_baseline.mp4"
OUTPUT = ROOT / "output/cycle621_CLEAN_SUBSCENE_WIPE_HUMAN_REVIEW.mp4"
START, END, LEFT, RIGHT, FPS = 244, 257, 241, 260, 30

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def get_frame(path, n):
    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, n)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError(f"Unable to decode frame {n}")
    return frame

def wipe_frame(before, after, index, start=START, end=END, accent=(218, 240, 80)):
    """Hard mask, not alpha blending. Accent is BGR."""
    if not start <= index <= end:
        raise ValueError("outside wipe")
    if before.shape != after.shape:
        raise ValueError("frame dimensions differ")
    height = before.shape[0]
    fraction = min(1.0, (index - start + 1) / 8.0)
    fraction = fraction * fraction * (3 - 2 * fraction)
    y = round(height * fraction)
    output = before.copy()
    output[:y, :, :] = after[:y, :, :]
    if y < 1300 and fraction < 1:
        output[max(0, y - 3):min(height, y + 3), :, :] = accent
    return output

def render(source=SOURCE, output=OUTPUT):
    source, output = Path(source), Path(output)
    config = json.loads((ROOT / "assets/genres.json").read_text())
    if len(config["genres"]) != 10:
        raise ValueError("Expected 10 genre configurations")
    before = get_frame(source, LEFT)
    after = get_frame(source, RIGHT)
    cap = cv2.VideoCapture(str(source))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if (width, height, frames) != (1080, 1920, 468):
        raise ValueError(f"Unexpected source video {(width, height, frames)}")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{width}x{height}",
        "-r", str(FPS), "-i", "pipe:0", "-i", str(source),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
        "-preset", "veryfast", "-crf", "17", "-threads", "2",
        "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart", str(output),
    ]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for n in range(frames):
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError(f"Source stopped at frame {n}")
            if START <= n <= END:
                frame = wipe_frame(before, after, n)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        stderr = proc.stderr.read().decode(errors="replace")
        if proc.wait():
            raise RuntimeError(stderr[-2000:])
    finally:
        cap.release()
    manifest = {
        "cycle": 621, "previous_cycle": 620,
        "change": "14-frame top-down non-blended intra-chapter wipe",
        "frames_changed": list(range(START, END + 1)),
        "source_stills": [LEFT, RIGHT],
        "genre_config_count": len(config["genres"]),
        "source_sha256": sha256(source), "output_sha256": sha256(output),
        "cost_jpy": 0, "status": "HUMAN_REVIEW",
        "publication": "NOT_APPROVED",
    }
    (output.parent / "render_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )
    return manifest

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    print(json.dumps(render(args.input, args.output), ensure_ascii=False, indent=2))
