"""Reusable zero-cost Japanese sentence-paced captions for ten TikTok genres.

Technical checks do not constitute rights clearance or human publishing approval.
"""
from dataclasses import dataclass

GENRES = (
    "ai_productivity", "beauty", "romance_psychology", "money_saving",
    "sales_business", "career", "health_lifestyle", "trivia_science",
    "travel_food", "product_lifestyle",
)
LINE_BREAKS = (
    ("AIで仕事を早くするなら、", "最初の一歩が大事。"),
    ("まず、繰り返している作業を", "書き出す。"),
    ("次に、完成形の見本を", "用意する。"),
    ("指示は、目的と条件を", "具体的に伝える。"),
    ("最初の出力は、", "必ず自分で確かめる。"),
    ("違いがあれば、修正点を", "一つずつ伝える。"),
    ("使える指示は、", "テンプレートに残す。"),
    ("小さな時短を、", "毎日の習慣にしよう。"),
)

@dataclass(frozen=True)
class Caption:
    start: float
    end: float
    text: str
    lines: tuple[str, str]

def captions_from_beats(beats, genre="ai_productivity"):
    if genre not in GENRES:
        raise ValueError("Unknown genre")
    if len(beats) != 24:
        raise ValueError("Expected 24 narration beats")
    out = []
    for i, (left, right) in enumerate(LINE_BREAKS):
        group = beats[3*i:3*i+3]
        text = "".join(str(b["text"]) for b in group)
        if text != left + right:
            raise ValueError(f"Slide {i+1}: caption does not preserve narration")
        if max(len(left), len(right)) > 16:
            raise ValueError("Caption too long for mobile")
        start, end = float(group[0]["start"]), float(group[-1]["end"])
        if not (0 <= start < end <= 23.04):
            raise ValueError("Invalid timing")
        out.append(Caption(start, end, text, (left, right)))
    if any(out[i].end > out[i+1].start for i in range(7)):
        raise ValueError("Overlapping captions")
    return tuple(out)

def ass_time(t):
    cs = round(t * 100)
    return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"

def ass_document(captions):
    header = """[Script Info]
Title: cycle874 sentence-paced Japanese subtitles - human review
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: JP,Noto Sans CJK JP,67,&H00FFFFFF,&H00FFFFFF,&H00321C13,&H90000000,-1,0,0,0,100,100,0,0,1,5,1,2,74,74,230,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for c in captions:
        text = "\\N".join(c.lines)
        events.append(f"Dialogue: 0,{ass_time(c.start)},{ass_time(c.end)},JP,,0,0,0,,{{\\fad(100,100)}}{text}")
    return header + "\n".join(events) + "\n"

def dwell_stats(captions, beats):
    old = sum(b["end"]-b["start"] for b in beats) / len(beats)
    new = sum(c.end-c.start for c in captions) / len(captions)
    return {"old_events": len(beats), "new_events": len(captions),
            "old_mean_s": round(old, 3), "new_mean_s": round(new, 3),
            "dwell_multiplier": round(new / old, 3)}
