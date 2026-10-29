"""Review-only Japanese TikTok loudness normalizer. No posting or paid APIs."""
from __future__ import annotations
import argparse, hashlib, json, math, re, subprocess
from pathlib import Path

GENRE_POLICIES = {
    "ai_work": (-16.0, -1.5), "business": (-16.0, -1.5),
    "finance": (-16.0, -1.5), "education": (-16.0, -1.5),
    "career": (-16.0, -1.5), "wellness": (-16.0, -1.5),
    "lifestyle": (-16.0, -1.5), "technology": (-16.0, -1.5),
    "travel": (-16.0, -1.5), "trivia": (-16.0, -1.5),
}
REVIEWED_GENRES = frozenset({"ai_work"})

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def run(cmd: list[str], timeout: int = 180) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f"ffmpeg failure {p.returncode}: {p.stderr[-1800:]}")
    return p.stderr

def loudness_report(path: Path, target_i: float, target_tp: float) -> dict:
    log = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
               "-map", "0:a:0", "-af",
               f"loudnorm=I={target_i}:TP={target_tp}:LRA=11:print_format=json",
               "-f", "null", "-"])
    m = re.search(r'\{\s*"input_i".*?\}', log, re.S)
    if not m:
        raise ValueError("EBU R128 measurement unavailable")
    report = json.loads(m.group(0))
    for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset"):
        if not math.isfinite(float(report[k])):
            raise ValueError(f"invalid audio measurement: {k}")
    return report

def video_digest(path: Path) -> str:
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path),
                        "-map", "0:v:0", "-c:v", "copy", "-f", "h264", "-"],
                       capture_output=True, timeout=120, check=True)
    return hashlib.sha256(p.stdout).hexdigest()

def probe(path: Path) -> dict:
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                        "-of", "json", str(path)], capture_output=True,
                       text=True, timeout=30, check=True)
    return json.loads(p.stdout)

def render(source: Path, output: Path, expected_sha: str, genre: str = "ai_work") -> dict:
    if genre not in GENRE_POLICIES:
        raise ValueError("unknown genre")
    if genre not in REVIEWED_GENRES:
        raise PermissionError("unreviewed genre blocked; human review required")
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
        raise ValueError("expected SHA-256 must be 64 lowercase hex digits")
    if not source.is_file() or sha256(source) != expected_sha:
        raise PermissionError("source SHA-256 mismatch; fail closed")
    if source.resolve() == output.resolve():
        raise ValueError("never overwrite source")
    ti, tp = GENRE_POLICIES[genre]
    source_probe = probe(source)
    source_audio = next(s for s in source_probe["streams"] if s["codec_type"] == "audio")
    source_audio_duration = float(source_audio["duration"])
    before = loudness_report(source, ti, tp)
    filt = (f"loudnorm=I={ti}:TP={tp}:LRA=11:"
            f"measured_I={before['input_i']}:measured_TP={before['input_tp']}:"
            f"measured_LRA={before['input_lra']}:"
            f"measured_thresh={before['input_thresh']}:"
            f"offset={before['target_offset']}:linear=true:print_format=json")
    # loudnorm may pad the tail. Trim to the original audio duration.
    filt += f",atrim=duration={source_audio_duration:.6f},asetpts=PTS-STARTPTS"
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        run(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", str(source),
             "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", filt,
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "1",
             "-metadata:s:a:0", "language=jpn", "-movflags", "+faststart",
             str(output)], timeout=180)
        after = loudness_report(output, ti, tp)
        video_same = video_digest(source) == video_digest(output)
        if not video_same:
            raise AssertionError("video bitstream changed unexpectedly")
        if abs(float(after["input_i"]) - ti) > 0.45:
            raise AssertionError("integrated loudness outside tolerance")
        if float(after["input_tp"]) > tp + 0.25:
            raise AssertionError("true peak exceeds ceiling")
        stream_info = probe(output)
        if float(stream_info["format"]["duration"]) > float(source_probe["format"]["duration"]) + 0.035:
            raise AssertionError("loudness filter padded video duration")
        v = next(s for s in stream_info["streams"] if s["codec_type"] == "video")
        a = next(s for s in stream_info["streams"] if s["codec_type"] == "audio")
        if (v["codec_name"], v["width"], v["height"], v["r_frame_rate"]) != ("h264", 1080, 1920, "30/1"):
            raise AssertionError("video specification mismatch")
        if (a["codec_name"], int(a["sample_rate"]), a["tags"].get("language")) != ("aac", 48000, "jpn"):
            raise AssertionError("audio specification mismatch")
        return {"cycle": 962, "source_sha256": expected_sha,
                "output_sha256": sha256(output), "genre": genre,
                "loudness_before": {k: before[k] for k in ("input_i", "input_tp", "input_lra")},
                "loudness_after": {k: after[k] for k in ("input_i", "input_tp", "input_lra")},
                "target_lufs": ti, "true_peak_ceiling_dbtp": tp,
                "video_bitstream_identical": video_same,
                "duration_s": float(stream_info["format"]["duration"]),
                "audio_language_tag": a["tags"].get("language"),
                "asr_verified": False, "rights_verified": False,
                "publication_approved": False}
    except Exception:
        output.unlink(missing_ok=True)
        raise

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--genre", default="ai_work")
    args = ap.parse_args()
    print(json.dumps(render(args.source, args.output, args.expected_sha256, args.genre),
                     ensure_ascii=False, indent=2))
