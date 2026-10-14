"""Cycle569: coordinates and timing for synthetic-video focus borders."""
WIDTH, HEIGHT = 1080, 1920
CUES = (
    ("result", 4.50, 5.55, (545, 870, 445, 185)),
    ("formula", 10.35, 11.55, (80, 550, 955, 150)),
    ("chart", 14.30, 15.65, (49, 1030, 978, 522)),
    ("verification", 16.55, 17.65, (75, 1300, 935, 290)),
)

def validate(cues=CUES):
    for name, start, end, (x, y, w, h) in cues:
        if not 0 <= start < end <= 20:
            raise ValueError("invalid timing")
        if not (35 <= x and x + w <= 1045 and 285 <= y and y + h <= 1610):
            raise ValueError("outside safe region")
    return True
