"""Cycle785: remove double-exposed text from known crossfade boundaries.

Review-only reimplementation, not the original v33 engine. Input rights
must be reviewed before publication. This tool never uploads media.
"""
import argparse
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np


def validate_plan(plan, fps, total_frames):
    windows = sorted(plan, key=lambda p: p["start"])
    last_end = -1
    for w in windows:
        s, e, a, b = (int(w[k]) for k in ("start", "end", "from", "to"))
        if not (0 <= a <= s < e < b < total_frames):
            raise ValueError(f"invalid transition endpoints: {w}")
        if s <= last_end:
            raise ValueError("overlapping transition windows")
        if e - s > int(round(fps * 0.5)):
            raise ValueError("transition longer than 0.5s")
        last_end = e
    return windows


def text_safe_cut(before, after, fraction):
    """Show one complete frame, never two text layers or a split seam."""
    if before.shape != after.shape or before.dtype != np.uint8:
        raise ValueError("endpoint frames must have matching uint8 shapes")
    return (before if fraction < 0.5 else after).copy()


def read_frame(capture, index):
    capture.set(cv2.CAP_PROP_POS_FRAMES, index)
    ok, frame = capture.read()
    if not ok:
        raise RuntimeError(f"cannot decode source frame {index}")
    return frame


def render(input_path, output_path, plan_path, work_dir):
    input_path, output_path, work_dir = map(Path, (input_path, output_path, work_dir))
    if "REVIEW_ONLY" not in output_path.name:
        raise ValueError("output must be explicitly REVIEW_ONLY")
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError("cannot open input MP4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if abs(fps - 30.0) > 0.01:
        raise ValueError(f"expected 30fps input, got {fps}")
    windows = validate_plan(plan, fps, count)
    work_dir.mkdir(parents=True, exist_ok=True)
    overlays = []
    for i, w in enumerate(windows):
        folder = work_dir / f"window_{i}"
        folder.mkdir(exist_ok=True)
        before = read_frame(cap, int(w["from"]))
        after = read_frame(cap, int(w["to"]))
        for n, _ in enumerate(range(int(w["start"]), int(w["end"]) + 1)):
            fraction = n / max(1, int(w["end"]) - int(w["start"]))
            frame = text_safe_cut(before, after, fraction)
            if not cv2.imwrite(str(folder / f"{n:04d}.png"), frame):
                raise RuntimeError("PNG write failed")
        overlays.append((folder, int(w["start"]), int(w["end"])))
    cap.release()
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(input_path)]
    for folder, _, _ in overlays:
        args += ["-framerate", "30", "-start_number", "0", "-i", str(folder / "%04d.png")]
    filters = []
    source = "[0:v]"
    for i, (_, start, end) in enumerate(overlays):
        label = f"[v{i}]"
        filters.append(f"[{i+1}:v]setpts=PTS-STARTPTS+{start}/30/TB[patch{i}]")
        filters.append(f"{source}[patch{i}]overlay=x=0:y=0:enable='between(n,{start},{end})':eof_action=pass{label}")
        source = label
    args += ["-filter_complex", ";".join(filters), "-map", source, "-map", "0:a:0",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
             "-r", "30", "-c:a", "copy", "-movflags", "+faststart", str(output_path)]
    subprocess.run(args, check=True)
    return {"input": str(input_path), "output": str(output_path), "fps": fps,
            "frames": count, "repaired_windows": windows, "rights_status": "unverified",
            "publication_approved": False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--plan", required=True)
    p.add_argument("--work-dir", required=True)
    a = p.parse_args()
    print(json.dumps(render(a.input, a.output, a.plan, a.work_dir),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
