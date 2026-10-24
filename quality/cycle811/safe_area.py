"""Cycle811: review-only, ten-genre TikTok subtitle safe-area contract.

This module defines native 1080x1920 caption bounds. It never posts videos.
Coordinates are design heuristics, NOT TikTok's officially verified UI bounds.
"""
WIDTH, HEIGHT, FPS = 1080, 1920, 30
RIGHT_UI_RESERVED_X = 890
BOTTOM_UI_RESERVED_Y = 1540
CAPTION_BOX = (70, 1140, 866, 1500)
AUTO_POST = False
EMPLOYEE_APPROVAL = False
GENRES = (
    "ai_work", "beauty", "love_psychology", "money_saving",
    "sales_business", "career", "health_life", "science",
    "travel_food", "product_life",
)
PALETTE = {
    "ai_work": "#5CB2FF", "beauty": "#FF85B4",
    "love_psychology": "#C78BFF", "money_saving": "#8ADEA1",
    "sales_business": "#58E5CE", "career": "#6FAFFF",
    "health_life": "#A4E48D", "science": "#76D7FA",
    "travel_food": "#F8C17C", "product_life": "#B8A4F8",
}
SENTENCE_CHUNKS = (
    ("仕事ができる人は、", "質問が", "違う。"),
    ("まず、", "目指すゴールを", "確認する。"),
    ("次に、", "今の数字を", "確かめる。"),
    ("そして、", "理想との差を", "一つに絞る。"),
    ("原因には、", "なぜを三回", "重ねる。"),
    ("対策は、", "今日できる行動に", "変える。"),
    ("結果を見て、", "また", "修正する。"),
    ("小さな改善が、", "強いチームを", "つくる。"),
)

def validate_caption_box(box=CAPTION_BOX):
    x0, y0, x1, y1 = box
    return (0 <= x0 < x1 < RIGHT_UI_RESERVED_X and
            0 <= y0 < y1 < BOTTOM_UI_RESERVED_Y)

def allocate_frames(total, chunks):
    """Allocate integer frames to 3 estimated caption phases with no frame loss."""
    if total < len(chunks) * 5:
        raise ValueError("scene duration too short")
    weights = [max(2, len(s.strip("、。"))) for s in chunks]
    available = total - len(chunks) * 5
    raw = [available * w / sum(weights) for w in weights]
    out = [5 + int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda j: raw[j] % 1, reverse=True)[:total-sum(out)]:
        out[i] += 1
    assert sum(out) == total
    return out

def validate_genre(genre):
    if genre not in GENRES:
        raise ValueError("unsupported genre")
    return PALETTE[genre]

def review_gate(approved=False, rights_verified=False, device_verified=False):
    """Always require human approval; no upload functionality is implemented."""
    return bool(approved and rights_verified and device_verified and EMPLOYEE_APPROVAL)
