#!/usr/bin/env python3
"""Two-pass, true-peak-safe narration mastering for existing 10-genre MP4s.

Preserves H.264 packets, chapter markers and burned-in Japanese captions.
No external media or cloud service is used. Review-only output.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

TARGET_I = -16.0
TARGET_TP = -1.5
TARGET_LRA = 11.0
GENRES = ("ai", "business", "money", "learning", "health", "food", "travel", "beauty", "career", "life")


def run(command):
    p = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(f"ffmpeg failed ({p.returncode}): {p.stderr[-2500:]}")
    return p


def loudness_measure(path):
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
             "-vn", "-af", f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json",
             "-f", "null", "-"])
    matches = re.findall(r'\{\s*"input_i"\s*:\s*".*?"\s*,.*?\}', p.stderr, re.S)
    if not matches:
        raise ValueError("loudnorm analysis JSON not found")
    return json.loads(matches[-1])


def video_duration(path):
    p = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)])
    return float(p.stdout.strip())


def master(input_path, output_path, stats_path=None, genre="ai"):
    if genre not in GENRES:
        raise ValueError(f"Unsupported genre: {genre}")
    source = Path(input_path)
    dest = Path(output_path)
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == dest.resolve():
        raise ValueError("input and output must be different")
    dest.parent.mkdir(parents=True, exist_ok=True)
    measured = loudness_measure(source)
    duration = video_duration(source)
    required = ["input_i", "input_tp", "input_lra", "input_thresh", "target_offset"]
    for k in required:
        if k not in measured or not float(measured[k]) == float(measured[k]):
            raise ValueError(f"Invalid first-pass measurement: {k}")
    filter_ = (f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}:"
               f"measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:"
               f"measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:"
               f"offset={measured['target_offset']}:linear=true:print_format=json")
    run(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", str(source),
         "-map", "0:v:0", "-map", "0:a:0", "-map_chapters", "0",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-af", filter_, "-metadata:s:a:0", "language=jpn",
         "-movflags", "+faststart", "-t", str(duration), str(dest)])
    after = loudness_measure(dest)
    report = {"genre": genre, "target_lufs": TARGET_I, "target_true_peak_dbtp": TARGET_TP,
              "before_lufs": float(measured["input_i"]),
              "after_lufs": float(after["input_i"]),
              "before_true_peak_dbtp": float(measured["input_tp"]),
              "after_true_peak_dbtp": float(after["input_tp"]),
              "before_lra": float(measured["input_lra"]),
              "after_lra": float(after["input_lra"]),
              "first_pass": measured, "second_pass": after}
    if abs(report["after_lufs"] - TARGET_I) > 0.4:
        raise RuntimeError(f"Integrated loudness outside 0.4 LU tolerance: {report['after_lufs']}")
    if report["after_true_peak_dbtp"] > TARGET_TP + 0.15:
        raise RuntimeError(f"True peak above tolerance: {report['after_true_peak_dbtp']}")
    if stats_path:
        Path(stats_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Review-only Japanese narration loudness mastering")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--report")
    p.add_argument("--genre", choices=GENRES, default="ai")
    a = p.parse_args()
    print(json.dumps(master(a.input, a.output, a.report, a.genre), indent=2, ensure_ascii=False))
