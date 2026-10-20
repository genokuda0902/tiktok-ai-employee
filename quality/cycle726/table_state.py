"""Shared synthetic table animation state (review only)."""
ROWS = (12, 15, 20, 18)
GENRES = ("ai_work", "beauty", "love_psychology", "saving",
          "sales_business", "career", "health", "science",
          "travel_food", "product_comparison")

def frame_state(frame, fps=30, rows=ROWS):
    if not rows or any(type(x) is not int or x < 0 for x in rows):
        raise ValueError("synthetic nonnegative integer rows required")
    if not 0 <= frame < 99:
        raise ValueError("frame out of range")
    t = frame / fps
    active = min(len(rows)-1, int(max(0, t-0.1)/0.65))
    progress = min(1.0, t/3.3)
    return active, progress
