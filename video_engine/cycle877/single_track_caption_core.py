"""Single-track ASS subtitles with active-phrase highlighting for 10 genres.

Prevents the duplicate subtitle collision found in cycle876.
Offline; timestamps are editorial, not ASR/phoneme-verified.
No posting, network, payment, or external assets.
"""
from __future__ import annotations

GENRES = (
    "ai_productivity", "beauty", "romance_psychology", "money_saving",
    "sales_business", "career", "health_lifestyle", "trivia_science",
    "travel_food", "product_lifestyle",
)
CAPTION_PANEL = (70, 1438, 1010, 1670)
CAPTION_CENTER = (540, 1554)


def ass_time(seconds):
    cs = round(seconds * 100)
    return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"


def escape_ass(value):
    return value.replace("\\", "＼").replace("{", "｛").replace("}", "｝").replace("\n", " ")


def validate_layout(genre):
    if genre not in GENRES:
        raise ValueError("unknown genre")
    x0, y0, x1, y1 = CAPTION_PANEL
    cx, cy = CAPTION_CENTER
    if not (0 <= x0 < cx < x1 <= 1080 and 0 <= y0 < cy < y1 <= 1920):
        raise ValueError("invalid safe-zone geometry")
    if min(cy-y0, y1-cy) < 95:
        raise ValueError("two-line caption lacks vertical padding")
    return True


def phrase_text(group, left, right, active):
    full = "".join(b["text"] for b in group)
    if full != left + right:
        raise ValueError("caption must preserve exact editorial text")
    if max(len(left), len(right)) > 16:
        raise ValueError("mobile caption line too long")
    start = sum(len(b["text"]) for b in group[:active])
    end = start + len(group[active]["text"])
    cut = len(left)
    points = sorted(set([0, len(full), start, end, cut]))
    chunks = []
    for a, b in zip(points, points[1:]):
        if a == cut:
            chunks.append(r"\N")
        color = r"{\c&H0000F9FF&}" if start <= a and b <= end else r"{\c&H00FFFFFF&}"
        chunks.append(color + escape_ass(full[a:b]))
    return "".join(chunks)


def events(beats, lines):
    if len(beats) != 24 or len(lines) != 8:
        raise ValueError("expected 24 beats and 8 complete sentences")
    result = []
    last_end = -1
    for i in range(8):
        group = beats[i*3:i*3+3]
        left, right = lines[i]
        for active, beat in enumerate(group):
            s, e = float(beat["start"]), float(beat["end"])
            if not 0 <= s < e <= 23.04 or s < last_end - 1e-7:
                raise ValueError("invalid or overlapping editorial beats")
            last_end = e
            text = phrase_text(group, left, right, active)
            result.append(
                f"Dialogue: 0,{ass_time(s)},{ass_time(e)},JP,,0,0,0,,"
                r"{\an5\pos(540,1554)}" + text
            )
    return tuple(result)


def make_ass(beats, lines, genre="ai_productivity"):
    validate_layout(genre)
    lines_out = events(beats, lines)
    header = """[Script Info]
Title: cycle877 - single-track safe Japanese captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: JP,Noto Sans CJK JP,66,&H00FFFFFF,&H00FFFFFF,&H00321C13,&H90000000,-1,0,0,0,100,100,0,0,1,4,0,5,74,74,366,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    return header + "\n".join(lines_out) + "\n"
