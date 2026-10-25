"""Review-only TikTok caption-beat progress renderer. No paid API or posting."""
import argparse
import json
import subprocess
from pathlib import Path

GENRES = {
    "ai_work": "&H00D0E134&",
    "sales_business": "&H2EE9FF&",
    "beauty": "&HCE83FF&",
    "romance": "&HFF80CB&",
    "saving": "&H80E2A5&",
    "career": "&HFFB770&",
    "wellness": "&H9DDD83&",
    "science": "&HFFD07E&",
    "travel_food": "&H8CDFFF&",
    "product_comparison_lifestyle": "&HFFB2CF&",
}
POLICY = {
    "review_only": True,
    "publication_approved": False,
    "automatic_posting": False,
    "external_upload": False,
    "source_rights_reviewed": False,
    "contains_personal_data": False,
}
TRACK_X, TRACK_Y, TRACK_W, TRACK_H = 77, 1338, 780, 10

def validate(beats, genre, manifest):
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError("Unsupported genre")
    if any(manifest.get(k) is not v for k, v in POLICY.items()):
        raise ValueError("Review-only policy mismatch")
    if len(beats) != 24:
        raise ValueError("Exactly 24 beats required for this input")
    previous_end = 0
    for beat in beats:
        start, end = float(beat["start"]), float(beat["end"])
        if not (0 <= previous_end <= start < end <= 23.034 and beat["text"].strip()):
            raise ValueError("Invalid beat")
        previous_end = end

def ass_time(t):
    centi = round(t * 100)
    seconds, cs = divmod(centi, 100)
    minutes, s = divmod(seconds, 60)
    hours, m = divmod(minutes, 60)
    return f"{hours}:{m:02d}:{s:02d}.{cs:02d}"

def generate_ass(beats, genre, manifest):
    validate(beats, genre, manifest)
    header = """[Script Info]
Title: cycle844 caption micro-progress - HUMAN REVIEW ONLY
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Shape,Noto Sans CJK JP,24,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    rect = f"m 0 0 l {TRACK_W} 0 l {TRACK_W} {TRACK_H} l 0 {TRACK_H}"
    for beat in beats:
        start, end = float(beat["start"]), float(beat["end"])
        duration_ms = max(1, round((end - start) * 1000))
        events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Shape,,0,0,0,,{{\\an7\\pos({TRACK_X},{TRACK_Y})\\p1\\1c&H4E5D63&\\alpha&H48&}}{rect}")
        events.append(f"Dialogue: 1,{ass_time(start)},{ass_time(end)},Shape,,0,0,0,,{{\\an7\\pos({TRACK_X},{TRACK_Y})\\p1\\1c{GENRES[genre]}\\fscx1\\t(0,{duration_ms},\\fscx100)}}{rect}")
    return header + "\n".join(events) + "\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--beats", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--genre", default="ai_work")
    args = parser.parse_args()
    beats = json.loads(Path(args.beats).read_text(encoding="utf-8"))
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    ass = Path(args.output).with_suffix(".ass")
    ass.parent.mkdir(parents=True, exist_ok=True)
    ass.write_text(generate_ass(beats, args.genre, manifest), encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-nostdin", "-y", "-loglevel", "error",
        "-i", args.source, "-vf", f"ass={ass}", "-c:v", "libx264",
        "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", "30", "-c:a", "copy", "-movflags", "+faststart",
        args.output,
    ], check=True, timeout=240)

if __name__ == "__main__":
    main()
