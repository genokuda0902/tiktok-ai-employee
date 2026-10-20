"""Cycle730: shared timing/data contract for fictional spreadsheet demonstrations."""
W, H, FPS = 1080, 1920, 30
START_FRAME, END_FRAME, TOTAL_FRAMES = 96, 195, 819
MONTHS = ("1月", "2月", "3月", "4月")
SALES = (12, 15, 20, 18)
GENRES = {
    "ai_work": "#65F4E9", "beauty": "#FFB9D4",
    "love_psychology": "#FFB1DE", "saving": "#A6E8B4",
    "sales_business": "#FFD390", "career": "#A4C7FF",
    "health": "#9DE6D4", "science": "#B2B6FF",
    "travel_food": "#FFC09D", "product_comparison": "#C3D0FF",
}
CAPTION_BOX = (55, 1210, 1025, 1550)

def visible_rows(local_frame):
    if not 0 <= local_frame < END_FRAME - START_FRAME:
        raise ValueError("Frame outside replacement scene")
    return min(4, int((local_frame / FPS) / 0.58) + 1)

def validate(genre):
    if genre not in GENRES or len(GENRES) != 10:
        raise ValueError("Unsupported genre")
    if (W, H, FPS) != (1080, 1920, 30):
        raise ValueError("Wrong video dimensions")
    if sum(SALES) != 65 or len(MONTHS) != len(SALES):
        raise ValueError("Fictional sales data invalid")
    x1, y1, x2, y2 = CAPTION_BOX
    if x1 < 0 or x2 > W or y1 < 1150 or y2 > 1560:
        raise ValueError("Unsafe caption bounds")
    return True

def publication_allowed(flags):
    required = ("rights", "privacy", "narration", "captions", "phone", "employee")
    return all(flags.get(key) is True for key in required) and flags.get("mode") == "MANUAL_ONLY"
