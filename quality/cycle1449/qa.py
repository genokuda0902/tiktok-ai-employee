"""Cross-genre timed beat and publication gates; review-only."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Review:
    duration: float
    scene_starts: tuple[float, ...]
    has_japanese_voice: bool
    captions_synced_to_voice: bool
    rights_approved: bool
    employee_approved: bool

def scene_beat(time_s: float, duration: float = 12.0, scene_length: float = 4.0) -> tuple[int, int]:
    if not 0 <= time_s < duration or scene_length <= 0:
        raise ValueError("time outside timeline")
    return int(time_s // scene_length), int((time_s % scene_length) // 1.0)

def can_publish(review: Review) -> bool:
    return bool(review.duration > 0 and review.scene_starts
        and review.scene_starts[0] == 0
        and tuple(sorted(set(review.scene_starts))) == review.scene_starts
        and review.scene_starts[-1] < review.duration
        and review.has_japanese_voice and review.captions_synced_to_voice
        and review.rights_approved and review.employee_approved)
