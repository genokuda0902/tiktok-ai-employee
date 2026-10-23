"""Timed Japanese caption highlighting for 1080x1920 image-slide videos.

Phrase-level timing only; this is NOT speech forced alignment.
No external APIs, paid services or automatic posting.
"""
from pathlib import Path

GENRE_RGB = {
    "science": "#35E8D2", "technology": "#80AAFF",
    "business": "#FFD176", "career": "#77E2C4",
    "finance": "#79D7FF", "history": "#F3BB81",
    "travel": "#6AE4C7", "food": "#FFA877",
    "health": "#77DBBD", "lifestyle": "#F0A5D8",
}
SEGMENTS = [
    ("この", "基板、"), ("実は", "パソコン。"),
    ("手のひら", "サイズ、"), ("でも", "本格派。"),
    ("画面に", "つなげば、"), ("操作", "できる。"),
    ("必要", "なのは、"), ("三つの", "接続。"),
    ("LED", "も"), ("光らせ", "られる。"),
    ("入力、", "処理、"), ("出力。",),
    ("最初", "は、"), ("たった", "一行。"),
    ("保存", "して、"), ("あとで", "試そう。"),
]

def ass_color(hex_rgb):
    s = hex_rgb.lstrip("#")
    if len(s) != 6 or any(c not in "0123456789abcdefABCDEF" for c in s):
        raise ValueError("Expected RGB hex")
    return "&H00" + s[4:6] + s[2:4] + s[:2]

def time_ass(t):
    if t < 0:
        raise ValueError("Negative time")
    cs = round(t * 100)
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def allocate_cs(start, end, pieces):
    total = round(end * 100) - round(start * 100)
    if total < len(pieces):
        raise ValueError("Cue too short")
    weights = [max(1, len(p)) for p in pieces]
    sizes = [max(1, round(total * w / sum(weights))) for w in weights]
    sizes[-1] += total - sum(sizes)
    if any(s <= 0 for s in sizes):
        raise ValueError("Invalid segment durations")
    return sizes

def escape_ass(text):
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")

def render_ass(cues, output, genre="science"):
    if genre not in GENRE_RGB:
        raise ValueError("Unknown genre")
    if len(cues) != len(SEGMENTS):
        raise ValueError("Expected 16 caption cues")
    color = ass_color(GENRE_RGB[genre])
    head = """[Script Info]
Title: cycle789 progressive Japanese captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Kinetic,Noto Sans CJK JP,70,""" + color + """,&H00FFFFFF,&H00131B19,&H00000000,-1,0,0,0,100,100,0,0,1,4,2,2,100,180,420,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    previous_end = -1.0
    for (start, end, label), parts in zip(cues, SEGMENTS):
        if start < previous_end or end <= start:
            raise ValueError("Invalid or overlapping cues")
        if "".join(parts) != label:
            raise ValueError(f"Caption mismatch: {label}")
        sizes = allocate_cs(start, end, parts)
        karaoke = "".join("{\\kf" + str(cs) + "}" + escape_ass(part)
                          for cs, part in zip(sizes, parts))
        head += (f"Dialogue: 0,{time_ass(start)},{time_ass(end)},"
                 f"Kinetic,,0,0,0,,{karaoke}\n")
        previous_end = end
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(head, encoding="utf-8")
    return head
