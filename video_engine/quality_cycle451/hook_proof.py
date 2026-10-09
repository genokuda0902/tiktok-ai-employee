"""Cycle451: genre-neutral, evidence-first hook contract. Review only.
Only fictional synthetic records; no posting or claim of Japanese narration.
"""
from dataclasses import dataclass
from typing import Tuple
import math

ROWS = (("D-201", False), ("D-202", False), ("D-203", True),
        ("D-204", False), ("D-205", False), ("D-206", True),
        ("D-207", False), ("D-208", False))

@dataclass(frozen=True)
class ProofHook:
    rows: Tuple[Tuple[str, bool], ...] = ROWS
    hook_seconds: float = 2.5
    fps: int = 30
    width: int = 1080
    height: int = 1920
    rights: str = "SELF_DRAWN_SYNTHETIC"
    publication: str = "NOT_APPROVED"
    auto_post: bool = False
    narration: str = "MISSING"

def validate(p: ProofHook) -> bool:
    if (p.width, p.height, p.fps) != (1080, 1920, 30):
        raise ValueError("Canvas must be 1080x1920@30")
    if not math.isfinite(p.hook_seconds) or p.hook_seconds != 2.5:
        raise ValueError("Hook duration must be exactly 2.5 seconds")
    if p.rights != "SELF_DRAWN_SYNTHETIC":
        raise ValueError("Assets must be self-drawn and synthetic")
    if p.publication != "NOT_APPROVED" or p.auto_post:
        raise ValueError("Publication and auto-post are prohibited")
    if p.narration not in ("MISSING", "VERIFIED"):
        raise ValueError("Narration must be explicitly missing or verified")
    if not p.rows or len(p.rows) > 12:
        raise ValueError("Expected 1-12 evidence rows")
    ids = [r[0] for r in p.rows]
    if len(ids) != len(set(ids)) or any(not x.startswith("D-") or not x[2:].isdigit() for x in ids):
        raise ValueError("Only unique fictional D-number IDs allowed")
    if any(type(flag) is not bool for _, flag in p.rows):
        raise ValueError("Status flags must be bool")
    if not any(flag for _, flag in p.rows):
        raise ValueError("At least one highlighted evidence row is required")
    return True

def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x*x*(3-2*x)

def hook_state(p: ProofHook, t: float) -> dict:
    validate(p)
    if not 0 <= t < p.hook_seconds:
        raise ValueError("Time out of hook range")
    move = ease((t-0.42)/0.83)
    selected = [i for i, (_, flag) in enumerate(p.rows) if flag]
    return {
        "move": move, "selected": selected, "count": len(selected),
        "total": len(p.rows), "reveal": ease((t-0.72)/0.55),
        "subtitle": "架空データ / 実際の業務は原本照合",
    }

def qa_gates(p: ProofHook) -> list[str]:
    validate(p)
    result = ["HUMAN_REVIEW", "PUBLICATION_NOT_APPROVED", "RIGHTS_REVIEW_REQUIRED"]
    if p.narration != "VERIFIED":
        result.extend(["JAPANESE_NARRATION_MISSING", "VOICE_CAPTION_SYNC_UNVERIFIED"])
    return result
