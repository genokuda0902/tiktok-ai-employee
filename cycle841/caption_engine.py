"""cycle841 shared engine: frame-exact, one-phrase Japanese captions.

Local finished MP4 and photo assets are review-only and deliberately not
committed to GitHub. No publishing, upload, billing or merge integration.
"""
from __future__ import annotations
import re

FPS = 30
WIDTH, HEIGHT = 1080, 1920
ORIGINAL_SCENE_FRAMES = (101, 93, 91, 99, 98, 101, 89, 103)
CUT_FRAMES = ((87,99),(178,190),(268,280),(368,380),
              (466,478),(566,578),(656,668))
BOUNDARIES = tuple(sum(ORIGINAL_SCENE_FRAMES[:i]) - 12*i for i in range(1,8))
SCENE_LENGTHS = tuple(b-a for a,b in zip((0,)+BOUNDARIES, BOUNDARIES+(691,)))
GENRE_PALETTES = {
    "ai_work":("#39E5D2","#F9DA62"),
    "sales_business":("#49D3FF","#FFE18A"),
    "beauty":("#F0A4D6","#FDE5A7"),
    "romance":("#FCA9B3","#FDE5A7"),
    "saving":("#7DE8B2","#FFDB7C"),
    "career":("#99BCFF","#FCE29D"),
    "wellness":("#90E0C6","#FFE7AB"),
    "science":("#A9ACFF","#F9D88A"),
    "travel_food":("#FFB677","#B4F2DE"),
    "product_comparison_lifestyle":("#C6ACFF","#FBEAA1"),
}
REQUIRED_POLICY = {
    "review_only": True,
    "publication_approved": False,
    "automatic_posting": False,
    "external_upload": False,
    "source_rights_reviewed": False,
    "contains_personal_data": False,
}

def require_review_only(manifest, genre):
    if genre not in GENRE_PALETTES or len(GENRE_PALETTES) != 10:
        raise ValueError("Unsupported genre")
    if not isinstance(manifest, dict) or any(
        manifest.get(key) != value for key, value in REQUIRED_POLICY.items()
    ):
        raise ValueError("Fail closed: unreviewed materials cannot be published")

def source_time(value):
    h, m, s = value.split(":")
    return int(h)*3600 + int(m)*60 + float(s)

def ass_time(seconds):
    cs = max(0, round(seconds*100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def map_cut_aware_time(seconds):
    frames = seconds * FPS
    removed = sum(max(0, min(frames,b)-a) for a,b in CUT_FRAMES if frames>a)
    return max(0,(frames-removed)/FPS)

def active_phrase(text):
    parts = text.split(r"\N")
    active = [part for part in parts if "&H00BEC637&" in part.upper()]
    if len(active) != 1:
        raise ValueError("Expected exactly one highlighted phrase")
    clean = re.sub(r"\{[^}]*\}", "", active[0]).strip()
    if not clean or len(clean)>18:
        raise ValueError("Unsafe subtitle length")
    return clean

def single_beat_captions(source_ass):
    beats = []
    for line in source_ass.splitlines():
        if not line.startswith("Dialogue:"):
            continue
        fields = line[len("Dialogue:"):].split(",",9)
        if len(fields) != 10:
            raise ValueError("Malformed ASS")
        start, end = map(source_time,fields[1:3])
        a, b = map_cut_aware_time(start), map_cut_aware_time(end)
        if b-a < 0.1 or b>691/FPS+0.02:
            raise ValueError("Caption outside video timeline")
        beats.append({"start":round(a,3),"end":round(b,3),
                      "text":active_phrase(fields[9])})
    if len(beats) != 24:
        raise ValueError("Expected 24 caption states")
    if any(x["end"]>y["start"]+0.045 for x,y in zip(beats,beats[1:])):
        raise ValueError("Caption overlap")
    return beats
