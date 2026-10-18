"""Cycle669: fail-closed Japanese narration timing for all ten genres.

No upload, no publication, no claims of human approval. Uses free Open JTalk
only when a Japanese dictionary and voice model are installed.
"""
from __future__ import annotations
import subprocess
import wave
from pathlib import Path

GENRES = ("AI・仕事効率化", "美容・身だしなみ", "恋愛・心理",
          "お金・節約", "営業・ビジネス", "転職・キャリア",
          "健康・生活改善", "雑学・科学", "旅行・グルメ",
          "商品比較・暮らし")

def wav_seconds(path):
    with wave.open(str(path), "rb") as stream:
        return stream.getnframes() / stream.getframerate()

def synthesize(text, wav_path, dictionary, voice):
    if not text or not text.strip():
        raise ValueError("Japanese narration text is required")
    for path in (dictionary, voice):
        if not Path(path).exists():
            raise FileNotFoundError(path)
    out = Path(wav_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["open_jtalk", "-x", str(dictionary), "-m", str(voice),
                    "-ow", str(out)], input=text, text=True, check=True)
    if wav_seconds(out) <= 0:
        raise RuntimeError("Generated voice is empty")
    return out

def validate_beats(genre, beats, margin=0.12):
    if genre not in GENRES:
        raise ValueError("Unknown genre")
    if not beats:
        raise ValueError("No beats")
    previous_end = 0.0
    for beat in beats:
        start = float(beat["start"])
        end = float(beat["end"])
        spoken = float(beat["spoken_seconds"])
        if start < previous_end or end <= start or spoken <= 0:
            raise ValueError("Invalid timeline")
        if spoken + margin > end - start:
            raise ValueError("Narration overflows its subtitle/scene window")
        if not beat["caption"].strip() or not beat["narration"].strip():
            raise ValueError("Missing Japanese text")
        previous_end = end
    return True

def review_status(beats):
    return {"quality": "HUMAN_REVIEW",
            "publication": "NOT_APPROVED",
            "manual_post_only": True,
            "voice_caption_sync_verified": False,
            "beats": len(beats)}
