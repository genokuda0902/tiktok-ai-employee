"""Reusable timing for a two-second answer-first opening hook.

No external assets or narration are included. Review only.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Hook:
    text: str
    start: float = 0.0
    end: float = 2.0

    def opacity(self, time_s: float) -> float:
        if time_s < self.start or time_s >= self.end:
            return 0.0
        return max(0.0, min(1.0, 1.0 - (time_s - self.start) / (self.end - self.start)))


def hook_for_sum(values: tuple[int, ...]) -> Hook:
    if not values or any(not isinstance(v, int) for v in values):
        raise ValueError("nonempty integer values required")
    return Hook(f"{sum(values):,} 円")
