"""Cycle749: offline review-only data and CTA contract (no publishing)."""
GENRES = ("ai_work", "romance", "beauty", "money", "trivia", "gadgets", "health", "sales", "travel", "mystery")
VALUES = (120000, 150000, 200000, 180000)
FORMULA = "=SUM(B2:B5)"
def verified_total(values=VALUES, formula=FORMULA):
    if len(values) != 4 or any(type(v) is not int or v < 0 for v in values):
        raise ValueError("four nonnegative integer values required")
    if formula != FORMULA:
        raise ValueError("formula does not match spreadsheet range")
    return sum(values)
def validate_genre(genre):
    if genre not in GENRES:
        raise ValueError("unsupported genre")
    return genre
