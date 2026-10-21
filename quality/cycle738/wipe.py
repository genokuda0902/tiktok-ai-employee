"""Zero-cost branded wipe for a 1080x1920 / 30fps video.
Preserves the original AAC narration, subtitles and video duration.
No automatic publishing; employee approval required.
"""
import argparse
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np

CUT_FRAMES = (58, 119, 178, 241, 281, 328, 376)
WIDTH, HEIGHT, FPS = 1080, 1920, 30
TRANSITION_FRAMES = 8
NAVY_BGR = (24, 18, 4)
MINT_BGR = (210, 218, 65)

def wipe_frame(frame, relative_frame):
    """No ghosted captions: use opaque brand-color wipe, never crossfade slides."""
    if not -4 <= relative_frame <= 3:
        return frame
    k = relative_frame + 5 if relative_frame < 0 else relative_frame + 1
    center = round(frame.shape[1] * k / 4)
    result = frame.copy()
    if relative_frame < 0:
        result[:, :center] = NAVY_BGR
    else:
        result[:, center:] = NAVY_BGR
    if center < frame.shape[1]:
        result[:, max(0, center-6):min(frame.shape[1], center+6)] = MINT_BGR
    return result

def render(source: Path, output: Path, cuts=CUT_FRAMES):
    cap = cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise RuntimeError("Cannot open source MP4")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if (w, h, n) != (WIDTH, HEIGHT, 429) or abs(fps-FPS) > 0.01:
        raise ValueError(f"Unexpected video input: {w}x{h} {fps}fps {n} frames")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}",
           "-r", str(FPS), "-i", "pipe:0", "-i", str(source),
           "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
           "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p",
           "-c:a", "copy", "-movflags", "+faststart", str(output)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    changed = 0
    try:
        for i in range(n):
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError(f"Decode ended at frame {i}")
            active = next((cut for cut in cuts if cut-4 <= i < cut+4), None)
            if active is not None:
                frame = wipe_frame(frame, i-active)
                changed += 1
            try:
                proc.stdin.write(frame.tobytes())
            except BrokenPipeError:
                raise RuntimeError("ffmpeg closed the encoder pipe")
        proc.stdin.close()
        err = proc.stderr.read().decode(errors="replace")
        rc = proc.wait()
        if rc:
            raise RuntimeError(f"Encoder failed ({rc}): {err[-2000:]}")
    finally:
        cap.release()
        if proc.poll() is None:
            proc.kill()
    return {"frames": n, "cuts": list(cuts), "modified_frames": changed,
            "audio": "AAC stream copy", "cost_yen": 0}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    print(json.dumps(render(a.source, a.output), ensure_ascii=False, indent=2))
