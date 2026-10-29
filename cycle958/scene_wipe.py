"""Review-only soft scene wipes for the eight-scene AI-work tutorial.

Reimplementation, not original v33. No media, audio, credentials, or release approvals
are bundled. Nine unreviewed genres deliberately fail closed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
ART_END = 1490  # Subtitle / voice-wave region below this stays untouched.
CUTS = (87, 174, 261, 348, 435, 522, 609)
WIPE_FRAMES = 9
SOURCE_SHA256 = "f270177b38a04a357fea3f86e6d70c1f8ef3da028004e1845b5f0310dca37e73"
GENRES = (
    "ai_work", "finance", "history", "science", "health", "travel",
    "food", "career", "education", "lifestyle",
)


def sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def validate(source: str | Path, genre: str, review_only: bool = True,
             publication_approved: bool = False) -> None:
    if genre not in GENRES:
        raise ValueError("unknown genre")
    if genre != "ai_work":
        raise ValueError("scene geometry and assets not reviewed for genre")
    if review_only is not True or publication_approved is not False:
        raise ValueError("publication is not approved; employee manual review required")
    if sha256(source) != SOURCE_SHA256:
        raise ValueError("source video SHA256 does not match the reviewed input")


def wipe_alpha(step: int, width: int = WIDTH, frames: int = WIPE_FRAMES,
               feather: int = 100) -> np.ndarray:
    """A progressive left-to-right wipe, with a soft feathered edge.

    Alpha=1 means new scene; 0 means frozen last frame of previous scene.
    The first frame reveals a small strip, and the last frame is fully new.
    """
    if not 0 <= step < frames or width <= 0 or frames < 2 or feather <= 0:
        raise ValueError("invalid wipe geometry")
    if step == frames - 1:
        return np.ones((1, width, 1), dtype=np.float32)
    center = -feather / 2 + (width + feather) * (step + 1) / frames
    x = np.arange(width, dtype=np.float32)
    z = np.clip((center - x + feather / 2) / feather, 0.0, 1.0)
    alpha = z * z * (3.0 - 2.0 * z)
    return alpha[None, :, None].astype(np.float32)


def wipe_art(previous: np.ndarray, current: np.ndarray, step: int,
             art_end: int = ART_END) -> np.ndarray:
    if previous.shape != current.shape or previous.ndim != 3 or previous.shape[2] != 3:
        raise ValueError("frames must be identically sized BGR images")
    if art_end <= 0 or art_end > current.shape[0]:
        raise ValueError("invalid subtitle protection boundary")
    alpha = wipe_alpha(step, current.shape[1])
    result = current.copy()
    a = previous[:art_end].astype(np.float32)
    b = current[:art_end].astype(np.float32)
    result[:art_end] = np.clip(a * (1.0 - alpha) + b * alpha, 0, 255).astype(np.uint8)
    return result


def render(source: str | Path, output: str | Path, genre: str = "ai_work") -> dict:
    validate(source, genre)
    source, output = Path(source), Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise RuntimeError("cannot decode source")
    geometry = (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                round(cap.get(cv2.CAP_PROP_FPS)))
    if geometry != (WIDTH, HEIGHT, FPS):
        cap.release()
        raise ValueError(f"unexpected source geometry {geometry}")
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
               "-pix_fmt", "bgr24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS),
               "-i", "pipe:0", "-i", str(source), "-map", "0:v:0", "-map", "1:a:0",
               "-frames:v", str(FRAMES), "-c:v", "libx264", "-preset", "veryfast",
               "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy",
               "-movflags", "+faststart", str(output)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    prior = None
    modified = 0
    try:
        for i in range(FRAMES):
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError(f"source truncated at frame {i}")
            original = frame.copy() if i in {c - 1 for c in CUTS} else None
            active = next((c for c in CUTS if c <= i < c + WIPE_FRAMES), None)
            if active is not None:
                if prior is None:
                    raise RuntimeError("previous scene snapshot missing")
                frame = wipe_art(prior, frame, i - active)
                modified += 1
            if original is not None:
                prior = original
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        error = proc.stderr.read().decode("utf-8", "replace")
        if proc.wait() != 0:
            raise RuntimeError(error[-3000:])
    except Exception:
        if proc.stdin and not proc.stdin.closed:
            proc.stdin.close()
        proc.kill()
        proc.wait()
        raise
    finally:
        cap.release()
    if modified != len(CUTS) * WIPE_FRAMES:
        raise RuntimeError("transition frame count mismatch")
    return {"source_sha256": sha256(source), "output_sha256": sha256(output),
            "frames": FRAMES, "modified_frames": modified, "cuts": list(CUTS),
            "wipe_frames_each": WIPE_FRAMES,
            "status": "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--qa", required=True)
    parser.add_argument("--genre", default="ai_work")
    args = parser.parse_args()
    result = render(args.source, args.output, args.genre)
    Path(args.qa).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
