"""Reusable zero-cost 10-genre TikTok subtitle/approval contract.

No auto-posting. Missing Japanese speech or human approval is always a hard fail.
"""
from __future__ import annotations

GENRES = (
    "AI・仕事効率化", "美容・身だしなみ", "恋愛・心理", "お金・節約",
    "営業・ビジネス", "転職・キャリア", "健康・生活改善",
    "雑学・科学", "旅行・グルメ", "商品比較・暮らし",
)
RESOLUTION = (1080, 1920)
SAFE_BOX = (75, 260, 900, 1535)
MAX_CAPTION_CHARS = 20

def validate_beats(beats):
    """Validate 8-scene/16-beat schema and subtitle timing without relying on TTS."""
    if len(beats) != 16:
        raise ValueError("exactly 16 caption beats required")
    end = 0.0
    for i, beat in enumerate(beats):
        if beat.get("scene") != i // 2 or beat.get("phase") != i % 2:
            raise ValueError(f"bad scene/phase at beat {i}")
        if abs(float(beat["start"]) - end) > .002:
            raise ValueError(f"caption gap/overlap at beat {i}")
        end = float(beat["end"])
        if end <= float(beat["start"]):
            raise ValueError(f"nonpositive beat {i}")
        if not (1 <= len(beat["caption"]) <= MAX_CAPTION_CHARS):
            raise ValueError(f"caption too long at beat {i}")
    if not 18 <= end <= 24:
        raise ValueError("video outside expected 18-24 second window")
    return end

def release_gate(qa):
    """Reject release until native Japanese speech and employee review are verified."""
    return all((
        qa.get("resolution") == [1080, 1920],
        qa.get("full_decode") == "PASS",
        qa.get("native_japanese_voice") == "HUMAN_VERIFIED",
        qa.get("voice_caption_sync") == "PASS",
        qa.get("human_review") == "APPROVED",
        qa.get("publication") == "MANUAL_POST_APPROVED",
    ))
