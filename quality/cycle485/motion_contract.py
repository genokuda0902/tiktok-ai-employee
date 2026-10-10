"""Genre-neutral, fail-closed visual evidence contract (review-only)."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite

SAFE_LEFT, SAFE_RIGHT = 64, 1016
SAFE_TOP, SAFE_BOTTOM = 250, 1560

@dataclass(frozen=True)
class EvidenceScene:
    topic: str
    values: tuple[int, ...]
    labels: tuple[str, ...]
    total: int
    start: float
    end: float
    bbox: tuple[int, int, int, int]
    provenance: str = 'SYNTHETIC_LOCAL'
    publication: str = 'NOT_APPROVED'
    auto_post: bool = False

def validate_scene(scene: EvidenceScene, duration: float) -> dict:
    if scene.publication != 'NOT_APPROVED' or scene.auto_post:
        raise ValueError('No automatic posting or preapproval')
    if scene.provenance != 'SYNTHETIC_LOCAL':
        raise ValueError('Source rights not allowlisted')
    if not scene.topic or len(scene.topic) > 42:
        raise ValueError('Topic required')
    if not scene.values or len(scene.values) != len(scene.labels) or len(scene.values) > 12:
        raise ValueError('Invalid series')
    if any(type(v) is not int or v < 0 for v in scene.values):
        raise ValueError('Values must be nonnegative integers')
    if any(not s or len(s) > 16 for s in scene.labels):
        raise ValueError('Invalid label')
    if sum(scene.values) != scene.total:
        raise ValueError('Evidence total mismatch')
    if not isfinite(duration) or duration <= 0 or not all(map(isfinite, (scene.start, scene.end))):
        raise ValueError('Nonfinite timing')
    if not 0 <= scene.start < scene.end <= duration:
        raise ValueError('Scene timing invalid')
    x0, y0, x1, y1 = scene.bbox
    if not (SAFE_LEFT <= x0 < x1 <= SAFE_RIGHT and SAFE_TOP <= y0 < y1 <= SAFE_BOTTOM):
        raise ValueError('TikTok UI safe area violation')
    return {'source_count': len(scene.values), 'verified_total': scene.total,
            'provenance': scene.provenance, 'publication': scene.publication,
            'auto_post': False, 'bounds': list(scene.bbox)}

def reveal_progress(t: float, start: float, duration: float) -> float:
    if not isfinite(t) or not isfinite(start) or not isfinite(duration) or duration <= 0:
        raise ValueError('Nonfinite or invalid animation')
    p = max(0.0, min(1.0, (t-start)/duration))
    return p*p*(3-2*p)
