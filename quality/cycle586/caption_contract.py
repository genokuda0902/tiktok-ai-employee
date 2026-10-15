"""Reusable safe-zone Japanese captions; no publication approval implied."""
from pathlib import Path
import re

MARGIN_BOTTOM = 300
MAX_CHARS = 12

def read_srt(path):
    cues = []
    raw = Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    for block in re.split(r"\n\s*\n", raw.strip()):
        lines = [x.strip() for x in block.splitlines() if x.strip()]
        if lines[0].isdigit():
            lines = lines[1:]
        if len(lines) < 2 or " --> " not in lines[0]:
            raise ValueError("invalid SRT")
        def to_ms(t):
            h, m, s, milli = map(int, re.split(r"[:,]", t))
            return ((h*60+m)*60+s)*1000+milli
        a, b = map(to_ms, lines[0].split(" --> "))
        txt = "".join(lines[1:])
        if not txt or any(x in txt for x in ["{", "}", "\\"]):
            raise ValueError("unsafe subtitle text")
        if not 0 <= a < b <= 20000 or (cues and a < cues[-1][1]):
            raise ValueError("invalid subtitle timing")
        cues.append((a, b, txt))
    return cues

def wrap(text):
    if len(text) <= MAX_CHARS:
        return text
    idx = min(MAX_CHARS, (len(text)+1)//2)
    for i, c in enumerate(text[:MAX_CHARS]):
        if c in "、。 ":
            idx = i+1
    if len(text)-idx > MAX_CHARS:
        raise ValueError("caption exceeds two lines")
    return text[:idx] + r"\N" + text[idx:]

def ass(cues):
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Noto Sans CJK JP,86,&H00FFFFFF,&H00FFFFFF,&H66071525,&H66071525,-1,0,0,0,100,100,0,0,3,10,0,2,145,195,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    def stamp(ms):
        s, c = divmod(ms//10,100)
        return f"{s//3600}:{s//60%60:02d}:{s%60:02d}.{c:02d}"
    return head + "".join(f"Dialogue: 0,{stamp(a)},{stamp(b)},Caption,,0,0,0,,{wrap(t)}\n" for a,b,t in cues)
