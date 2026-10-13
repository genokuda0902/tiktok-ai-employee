"""Free, caption-aware eight-scene transition planning for TikTok vertical videos.
Video assembly uses local FFmpeg only. Original Japanese AAC audio is stream-copied.
No automatic publishing or external asset requests.
"""
from pathlib import Path
import subprocess
import cv2
import numpy as np

GENRES = ("AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
          "営業・ビジネス", "転職・キャリア", "健康・生活改善",
          "雑学・科学", "旅行・グルメ", "商品比較・暮らし")

def detect_cuts(path, threshold=12.0, min_gap=18):
    cap = cv2.VideoCapture(str(path))
    last, cuts, n = None, [], 0
    while True:
        ok, frame = cap.read()
        if not ok: break
        small = cv2.resize(frame, (180, 320))
        if last is not None:
            d = np.abs(small.astype(np.int16) - last.astype(np.int16)).mean()
            if d >= threshold and (not cuts or n - cuts[-1] >= min_gap):
                cuts.append(n)
        last, n = small, n + 1
    cap.release()
    if n < 2: raise ValueError("No decodable frames")
    return cuts, n

def make_filter(cuts, frames, fps=30, half=3):
    bounds = [0] + list(cuts) + [frames]
    expr = []
    for i in range(len(bounds)-1):
        begin, end = bounds[i:i+2]
        start = f"start_mode=clone:start_duration={half/fps:.6f}:" if i else ""
        stop = f"stop_mode=clone:stop_duration={half/fps:.6f}" if i < len(bounds)-2 else "stop_mode=clone:stop_duration=0"
        expr.append(f"[0:v]trim=start_frame={begin}:end_frame={end},setpts=PTS-STARTPTS,fps={fps},tpad={start}{stop},settb=1/{fps},format=yuv420p[s{i}]")
    prev = "s0"
    for i, cut in enumerate(cuts):
        expr.append(f"[{prev}][s{i+1}]xfade=transition=fade:duration={2*half/fps:.6f}:offset={(cut-half)/fps:.6f}[x{i}]")
        prev = f"x{i}"
    expr.append(f"[{prev}]format=yuv420p[v]")
    return ";".join(expr)

def render(input_mp4, output_mp4):
    cuts, frames = detect_cuts(input_mp4)
    if not cuts: raise ValueError("No scene boundaries found")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(input_mp4), "-filter_complex", make_filter(cuts, frames),
        "-map", "[v]", "-map", "0:a:0", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-frames:v", str(frames), "-movflags", "+faststart", str(output_mp4)],
        check=True)
    return {"cuts": cuts, "frames": frames, "genres": len(GENRES), "review": "HUMAN_REVIEW"}
