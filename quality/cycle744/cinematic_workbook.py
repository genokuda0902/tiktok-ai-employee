"""Cycle744 reusable synthetic workbook scene core (review only).

Local MP4 renderer includes additional lighting/parallax layers, preserved in
the downloadable source ZIP. This module is the CI-friendly shared contract.
No confidential or third-party media.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, FRAMES = 1080, 1920, 30, 99
START, END = 3.2, 6.5
DATA = (("1月", 12), ("2月", 15), ("3月", 20), ("4月", 18))
PALETTES = {
    "ai_work": (46,232,231), "sales": (255,176,77),
    "business": (135,181,255), "finance": (148,232,122),
    "career": (255,141,171), "study": (183,149,255),
    "health": (97,223,171), "travel": (102,193,255),
    "food": (255,195,105), "lifestyle": (255,153,207),
}
def ease(x):
    x = max(0.0, min(1.0, float(x)))
    return x*x*(3-2*x)

def validate_data(data=DATA):
    if len(data) != 4 or any(
        not isinstance(month, str) or not month
        or type(value) is not int or value < 0
        for month, value in data
    ):
        raise ValueError("four fictional nonnegative integer months required")
    return sum(value for _, value in data)

def validate_provenance(metadata):
    if (metadata.get("source_kind") != "synthetic_demo"
        or metadata.get("release") != "NOT_APPROVED"
        or metadata.get("auto_post") is not False):
        raise ValueError("unapproved source or publication state")
    return True

def safe_regions():
    return {
        "title": (74,252,1000,404),
        "workbook": (105,490,978,1320),
        "caption": (70,1405,1008,1650),
    }

def verify_safe_regions():
    for name, (x1,y1,x2,y2) in safe_regions().items():
        if x1 < 40 or x2 > W-40 or y1 < 192 or y2 > H-230:
            raise ValueError("unsafe region: "+name)
    return True

def preview(t, genre="ai_work"):
    """Portable review frame; full cinematic scene renderer is in the ZIP."""
    if genre not in PALETTES or not 0 <= t < END-START:
        raise ValueError("invalid genre or time")
    validate_data()
    verify_safe_regions()
    accent = PALETTES[genre]
    im = Image.new("RGB", (W,H), (7,27,46))
    d = ImageDraw.Draw(im)
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    def label(xy, text, size, color):
        if Path(font_path).exists():
            f = ImageFont.truetype(font_path, size)
        else:
            f = ImageFont.load_default()
        d.text(xy,text,font=f,fill=color)
    label((80,290),"4か月の売上データ",66,"white")
    d.rounded_rectangle((110,490,970,1280),radius=30,
                        fill=(225,244,247),outline=accent,width=7)
    label((160,535),"月別売上データ｜サンプル",40,(19,70,80))
    for i,(month,value) in enumerate(DATA):
        y=670+i*130
        visible=ease((t-.2-i*.52)/.52)
        if visible>0:
            label((180,y),month,43,(23,63,77))
            label((630,y),str(value)+"万円",43,(20,82,89))
    d.rounded_rectangle((80,1430,1000,1630),radius=25,
                        fill=(4,18,35),outline=accent,width=4)
    label((120,1460),"まず、架空の四か月",56,"white")
    label((120,1530),"データを用意。",56,accent)
    return im
