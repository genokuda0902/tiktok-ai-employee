"""Zero-cost phrase-timestamp validation and subtitle cue generation.

The timestamps are editorial metadata, not ASR or phoneme alignment.
No network access, publishing, or external services.
"""
from __future__ import annotations

GENRES = (
    "ai_productivity", "beauty", "romance_psychology", "money_saving",
    "sales_business", "career", "health_lifestyle", "trivia_science",
    "travel_food", "product_lifestyle",
)
STAGE_LABELS = ("整理", "書き出す", "見本", "指示", "確認", "修正", "保存", "習慣")


def validate_beats(beats):
    if len(beats) != 24:
        raise ValueError("Exactly 24 editorial phrase beats required")
    for index, beat in enumerate(beats):
        start, end, phrase = beat["start"], beat["end"], beat["text"]
        if not (0 <= start < end <= 23.04):
            raise ValueError("Invalid timestamp")
        if not isinstance(phrase, str) or not phrase.strip() or len(phrase) > 16:
            raise ValueError("Invalid phrase")
        if index and beats[index - 1]["end"] > start:
            raise ValueError("Overlapping beats")
    return True


def ass_time(seconds):
    centis = round(seconds * 100)
    return f"{centis // 360000}:{centis // 6000 % 60:02d}:{centis // 100 % 60:02d}.{centis % 100:02d}"


def phrase_events(beats):
    validate_beats(beats)
    lines = []
    for beat in beats:
        phrase = beat["text"].replace("\\", "").replace("{", "").replace("}", "")
        lines.append(
            f"Dialogue: 1,{ass_time(beat['start'])},{ass_time(beat['end'])},"
            f"BEAT,,0,0,0,,{{\\an8\\pos(540,1734)\\fad(45,45)}}{phrase}"
        )
    return tuple(lines)


def navigation_state(stage, genre):
    if genre not in GENRES:
        raise ValueError("Unknown genre")
    if not 1 <= stage <= 8:
        raise ValueError("Stage out of range")
    return {"stage": stage, "total": 8, "label": STAGE_LABELS[stage - 1],
            "filled": tuple(index < stage for index in range(8))}
