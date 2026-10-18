"""Generic safe-area validation for a moving Before/After proof cue."""
def validate(cue, width=1080, height=1920, duration=20):
    if set(cue) != {"start", "end", "x0", "x1", "y", "h"}:
        raise ValueError("invalid cue schema")
    s, e = float(cue["start"]), float(cue["end"])
    x0, x1, y, h = (int(cue[k]) for k in ("x0", "x1", "y", "h"))
    if not (0 <= s < e <= duration and 60 <= x0 < x1 <= width-60):
        raise ValueError("invalid cue time or horizontal position")
    if not (180 <= y and h >= 10 and y+h <= height-320):
        raise ValueError("outside caption safe region")
    return True
