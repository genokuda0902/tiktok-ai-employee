#!/usr/bin/env python3
"""Cycle610: free local two-pass audio loudness pass; preserve video stream."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "assets/cycle609_baseline.mp4"
DEFAULT_OUTPUT = ROOT / "output/cycle610_LOUDNESS_CONSISTENCY_HUMAN_REVIEW.mp4"
TARGET_I, TARGET_TP, TARGET_LRA = -16.0, -1.5, 11.0
GENRES = ("AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
          "営業・ビジネス", "転職・キャリア", "健康・生活改善",
          "雑学・科学", "旅行・グルメ", "商品比較・暮らし")

def run(args):
    return subprocess.run(args, check=True, text=True, capture_output=True, timeout=180)

def parse_loudnorm(log):
    matches = re.findall(r'\{\s*"input_i"\s*:.*?\}', log, re.S)
    if not matches:
        raise ValueError("Missing loudnorm JSON")
    return json.loads(matches[-1])

def measure(path):
    return parse_loudnorm(run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
      "-map", "0:a:0", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
      "-f", "null", "-"]).stderr)

def filter_for(m):
    for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset"):
        float(m[k])
    return ("loudnorm=I=-16:TP=-1.5:LRA=11:"
       f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
       f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
       f"offset={m['target_offset']}:linear=true:print_format=json,aresample=48000")

def render(source, output, genre="雑学・科学"):
    if genre not in GENRES:
        raise ValueError("Unknown genre")
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    before = measure(source)
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
         "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
         "-af", filter_for(before), "-c:a", "aac", "-b:a", "192k",
         "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(output)])
    after = measure(output)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return {"path": str(output), "sha256": digest, "before_lufs": before["input_i"],
            "after_lufs": after["input_i"], "status": "HUMAN_REVIEW",
            "publication": "NOT_APPROVED"}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--genre", default="雑学・科学")
    a = p.parse_args()
    print(json.dumps(render(a.input, a.output, a.genre), ensure_ascii=False))
