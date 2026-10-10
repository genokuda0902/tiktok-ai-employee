"""Validate synthetic proof scenes before rendering."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ProofBeat:
    start: float
    end: float
    label: str
    source_kind: str
    source_values: tuple
    claimed_total: int
    safe_bbox: tuple

def validate_proof_beat(beat, video_duration, source_rights, publication="NOT_APPROVED", auto_post=False):
    if source_rights not in ("SYNTHETIC_LOCAL", "USER_OWNED_REVIEW_ONLY"):
        raise ValueError("rights")
    if publication != "NOT_APPROVED" or auto_post:
        raise ValueError("publication")
    if beat.source_kind != "SYNTHETIC_DEMO":
        raise ValueError("source")
    if not beat.label or len(beat.label) > 36:
        raise ValueError("label")
    if not 0 <= beat.start < beat.end <= video_duration:
        raise ValueError("timing")
    if not beat.source_values or len(beat.source_values) > 24:
        raise ValueError("values")
    if any(type(v) is not int or v < 0 for v in beat.source_values):
        raise ValueError("value type")
    if sum(beat.source_values) != beat.claimed_total:
        raise ValueError("total mismatch")
    x0,y0,x1,y1=beat.safe_bbox
    if not (64 <= x0 < x1 <= 1016 and 250 <= y0 < y1 <= 1570):
        raise ValueError("safe area")
    return {"total":beat.claimed_total,"source_count":len(beat.source_values),"provenance":beat.source_kind,"publication":publication,"auto_post":False}
