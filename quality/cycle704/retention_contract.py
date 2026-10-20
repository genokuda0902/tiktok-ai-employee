"""Cross-genre first-second verified proof and publication safety (cycle704).
Review-only. This module does not authorize posting or reuse of reference images.
"""
from dataclasses import dataclass
from math import isfinite

GENRES = ("AI仕事効率化", "AIツール紹介", "Excel活用", "ビジネススキル", "副業知識",
          "デザイン", "教育", "科学", "ガジェット", "生活効率化")
SCENE_DURATIONS = (2.0, 2.0, 2.5, 2.5, 2.5, 2.5, 3.0, 3.0)
ROWS = (("赤", 1200), ("青", 2500), ("緑", 1000), ("青", 3500))

@dataclass(frozen=True)
class Beat:
    start: float
    end: float
    kind: str

def beats():
    kinds = ("proof_hook", "problem", "prompt", "answer", "type", "select", "verify", "cta")
    cursor = 0.0
    result = []
    for kind, seconds in zip(kinds, SCENE_DURATIONS):
        result.append(Beat(cursor, cursor + seconds, kind))
        cursor += seconds
    return tuple(result)

def verified_sumif(rows=ROWS, color="青"):
    if not rows or any(not isinstance(n, int) or n < 0 for _, n in rows):
        raise ValueError("invalid fictional demonstration data")
    return sum(n for key, n in rows if key == color)

def proof_hook(t, value=6000):
    if not isfinite(t) or not 0 <= t < 20:
        raise ValueError("invalid timestamp")
    if value != verified_sumif():
        raise ValueError("unverified numeric hook")
    return {"visible": t < 2.0, "value": value, "start": 0.0, "deadline": 1.0}

def safe_caption(box, width=540, height=960):
    x0, y0, x1, y1 = box
    return 24 <= x0 < x1 <= width-72 and 90 <= y0 < y1 <= height-195

def narration_status(audio_streams, japanese_speech_generated):
    return "JA_SPEECH_VERIFIED" if audio_streams and japanese_speech_generated else "BGM_ONLY_NOT_JA"

def release_gate(approved_assets, no_private_data, narration_present,
                 speech_sync_verified, employee_approved, phone_checked):
    return "MANUAL_POST_REVIEWED" if all((approved_assets, no_private_data,
            narration_present, speech_sync_verified, employee_approved,
            phone_checked)) else "PUBLICATION_NOT_APPROVED"
