"""Review-only image-first depth cue for the *verified* AI-work scene03 geometry.

No input image, audio, captions or personal media is committed to GitHub.
Fail closed for unknown geometry/genre; this is NOT v33 equivalence or publication approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np

WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENE_START, SCENE_END = 5.8, 8.7
# A configuration registry, not proof that ten layouts were visually approved.
GENRE_PRESETS = {
    "ai_work": (0.74, (7, 25, 34)),
    "work_skills": (0.72, (14, 28, 43)),
    "finance": (0.66, (20, 29, 32)),
    "career": (0.70, (20, 23, 40)),
    "education": (0.64, (22, 28, 38)),
    "health": (0.62, (18, 31, 31)),
    "lifestyle": (0.58, (29, 29, 29)),
    "travel": (0.60, (25, 31, 37)),
    "food": (0.58, (22, 31, 36)),
    "technology": (0.73, (15, 27, 38)),
}
# Verified ONLY for the private cycle952 AI-work video, scene03.
APPROVED_GEOMETRY = {
    "ai_work": {
        "source_sha256": "0f270382d848e9c89d9e75bcad7815fc61f01ca2a9f8c7d5c0f2c04de2dacd82",
        "paper_polygon": ((90, 310), (895, 310), (895, 1135), (90, 1135)),
    }
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def validate_source(path: Path, genre: str, expected_sha: str | None = None) -> str:
    if genre not in GENRE_PRESETS:
        raise ValueError("Unsupported genre")
    if genre not in APPROVED_GEOMETRY:
        raise ValueError("Geometry unreviewed for this genre: fail closed")
    actual = sha256_file(path)
    pinned = APPROVED_GEOMETRY[genre]["source_sha256"]
    if actual != pinned or (expected_sha is not None and actual != expected_sha):
        raise ValueError("Source hash mismatch: refusing to alter unreviewed media")
    return actual

def temporal_strength(t: float) -> float:
    if t < SCENE_START or t >= SCENE_END:
        return 0.0
    return max(0.0, min(1.0, (t - SCENE_START) / 0.32,
                        (SCENE_END - t) / 0.32))

def make_mask(genre: str, width: int = WIDTH, height: int = HEIGHT) -> np.ndarray:
    if genre not in APPROVED_GEOMETRY or (width, height) != (WIDTH, HEIGHT):
        raise ValueError("unreviewed geometry or video dimensions")
    paper = np.zeros((height, width), dtype=np.uint8)
    polygon = np.array(APPROVED_GEOMETRY[genre]["paper_polygon"], np.int32)
    cv2.fillPoly(paper, [polygon], 255)
    paper = cv2.GaussianBlur(paper, (0, 0), 9).astype(np.float32) / 255.0
    # Only the scene image area is altered. Top heading and subtitle/footer untouched.
    vertical = np.zeros((height,), np.float32)
    vertical[355:1160] = 1.0
    vertical[335:355] = np.linspace(0, 1, 20, endpoint=False)
    vertical[1160:1200] = np.linspace(1, 0, 40, endpoint=False)
    return np.clip((1 - paper) * vertical[:, None], 0, 1)

def transform(frame: np.ndarray, t: float, genre: str, mask: np.ndarray) -> np.ndarray:
    if frame.shape != (HEIGHT, WIDTH, 3):
        raise ValueError("Expected 1080x1920 BGR frame")
    strength = temporal_strength(t)
    if strength == 0:
        return frame.copy()
    intensity, tint = GENRE_PRESETS[genre]
    # Crop-only blur for performance. The paper region stays pixel-identical.
    y0, y1 = 300, 1200
    roi = frame[y0:y1]
    blurred = cv2.GaussianBlur(roi, (0, 0), sigmaX=13, sigmaY=13)
    tinted = cv2.addWeighted(blurred, 0.87, np.full_like(roi, tint), 0.13, 0)
    alpha = (mask[y0:y1] * (strength * intensity))[:, :, None]
    output = frame.copy()
    output[y0:y1] = np.clip(roi.astype(np.float32) * (1 - alpha)
                              + tinted.astype(np.float32) * alpha, 0, 255).astype(np.uint8)
    return output

def probe(path: Path) -> dict:
    data = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
    ]))
    return data

def render(source: Path, target: Path, genre: str = "ai_work") -> dict:
    digest = validate_source(source, genre)
    metadata = probe(source)
    video = next(s for s in metadata["streams"] if s["codec_type"] == "video")
    audio = next(s for s in metadata["streams"] if s["codec_type"] == "audio")
    if (video["width"], video["height"], video["r_frame_rate"]) != (WIDTH, HEIGHT, "30/1"):
        raise ValueError("Unexpected video dimensions or frame rate")
    if audio["codec_name"] != "aac" or int(audio["sample_rate"]) != 48000:
        raise ValueError("Unexpected source audio format")
    target.parent.mkdir(parents=True, exist_ok=True)
    decoder = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", str(source),
                                "-map", "0:v:0", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                               stdout=subprocess.PIPE)
    encoder = subprocess.Popen([
        "ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
        "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-", "-i", str(source),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
        str(target)
    ], stdin=subprocess.PIPE)
    mask = make_mask(genre)
    size = WIDTH * HEIGHT * 3
    frames = 0
    changed = 0
    try:
        while True:
            raw = decoder.stdout.read(size)
            if not raw:
                break
            if len(raw) != size:
                raise RuntimeError("Truncated frame")
            frame = np.frombuffer(raw, dtype=np.uint8).reshape(HEIGHT, WIDTH, 3)
            t = frames / FPS
            if temporal_strength(t) > 0:
                frame = transform(frame, t, genre, mask)
                changed += 1
            encoder.stdin.write(frame.tobytes())
            frames += 1
    finally:
        if decoder.stdout:
            decoder.stdout.close()
        if encoder.stdin:
            encoder.stdin.close()
        decoder_rc = decoder.wait()
        encoder_rc = encoder.wait()
    if decoder_rc or encoder_rc or frames != 691 or changed < 60:
        raise RuntimeError(f"Rendering incomplete: decoder={decoder_rc} encoder={encoder_rc} frames={frames} changed={changed}")
    return {"source_sha256": digest, "output_sha256": sha256_file(target),
            "frames": frames, "changed_frames": changed, "genre": genre,
            "publication_approved": False}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--genre", default="ai_work")
    args = parser.parse_args()
    print(json.dumps(render(args.source, args.output, args.genre), indent=2))
