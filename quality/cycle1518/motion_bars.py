"""Reusable easing for animated comparison bars. No publication approval implied."""
def progress_at(time_s: float, index: int, *, start: float = 0.5, stagger: float = 0.45, duration: float = 1.2) -> float:
    if duration <= 0 or index < 0:
        raise ValueError("invalid animation configuration")
    x = max(0.0, min(1.0, (time_s - (start + index * stagger)) / duration))
    return 1.0 - (1.0 - x) ** 3

def bar_width(value: float, progress: float, *, full_width: int = 470) -> int:
    if not 0 <= value <= 100 or not 0 <= progress <= 1 or full_width <= 0:
        raise ValueError("invalid bar")
    return int(full_width * value / 100 * progress)
