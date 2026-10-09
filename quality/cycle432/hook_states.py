"""cycle432 reusable kinetic hook state contract for 10 genres."""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class HookState:
    at_seconds: float
    label: str
    active_index: int

def three_phase_hook(labels: Sequence[str]) -> list[HookState]:
    if len(labels) != 3 or any(not label.strip() for label in labels):
        raise ValueError("Exactly three nonempty hook lines required")
    return [HookState(i * 0.5, labels[i], i) for i in range(3)]

if __name__ == "__main__":
    for phase in three_phase_hook(["集中が切れた","気合いで続ける？","まず、切り替える"]):
        print(phase)
