"""Review-only manifest and media validation for all ten genres."""
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = ("ai_productivity", "trivia", "cooking", "beauty", "finance",
          "wellness", "travel", "product_demo", "story", "business")

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            h.update(block)
    return h.hexdigest()

def check(source, manifest):
    m = json.loads(Path(manifest).read_text(encoding="utf-8"))
    expected = {"quality_approved": False, "publication_approved": False,
                "publish_mode": "employee_manual_only",
                "source_rights": "unverified_review_only",
                "audio_rights": "unverified_review_only",
                "caption_kind": "scene_summary_not_verbatim_transcript"}
    if any(m.get(k) != v for k, v in expected.items()):
        raise ValueError("review-only approval gate failed")
    if m.get("genre_id") not in GENRES or m.get("source_sha256") != digest(source):
        raise ValueError("genre or input SHA invalid")
    p = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                        "-of", "json", str(source)], check=True, capture_output=True, text=True)
    info = json.loads(p.stdout)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    kinds = {s["codec_type"] for s in info["streams"]}
    if (video["width"], video["height"]) != (1080, 1920) or not {"video", "audio", "subtitle"}.issubset(kinds):
        raise ValueError("media streams invalid")
    beats = m.get("beats", [])
    if not 3 <= len(beats) <= 10 or beats[0]["start"] != 0:
        raise ValueError("invalid beats")
    for i, beat in enumerate(beats):
        if beat["end"] <= beat["start"] or (i and abs(beat["start"]-beats[i-1]["end"]) > .002):
            raise ValueError("non-contiguous beats")
    if abs(beats[-1]["end"] - float(info["format"]["duration"])) > .04:
        raise ValueError("beat duration mismatch")
    return m, info
