"""Shared short-form scene timing. Review-only: no publishing authorization."""
from bisect import bisect_right

BOUNDARIES = (0.0, 1.5, 5.0, 8.5, 12.0)

def scene_index(seconds: float, boundaries=BOUNDARIES) -> int:
    """First 1.5 seconds reserved for hook; never index past final scene."""
    if not 0 <= seconds < boundaries[-1]:
        raise ValueError("timestamp outside video")
    if len(boundaries) < 2 or boundaries[0] != 0 or any(a >= b for a,b in zip(boundaries,boundaries[1:])):
        raise ValueError("invalid scene boundaries")
    return bisect_right(boundaries, seconds) - 1

def publication_allowed(narration_verified=False, synced_captions=False, rights_approved=False, human_approved=False):
    return all((narration_verified, synced_captions, rights_approved, human_approved))
