"""Cycle457 reusable synthetic proof contract. Review-only, no posting.
The local MP4 renderer is a reimplementation, not original v33 code.
"""
from dataclasses import dataclass

ROWS = [
    ("04/01", "A", 12), ("04/02", "B", 8),
    ("04/03", "A", 9), ("04/04", "B", 11),
    ("04/05", "A", 14), ("04/06", "B", 7),
]
SCENES = (
    (0, 2, "HOOK"), (2, 5, "INPUT"), (5, 9, "TRANSFORM"),
    (9, 12, "PROOF"), (12, 15, "RESULT"),
    (15, 18, "COMPARE"), (18, 20, "CTA"),
)
SUMIF_FORMULA = '=SUMIF(B4:B9,"A",C4:C9)'
RIGHTS = "SYNTHETIC_ORIGINAL"
PUBLICATION = "NOT_APPROVED"
AUTO_POST = False

@dataclass(frozen=True)
class QualityState:
    japanese_voice_verified: bool = False
    semantic_caption_sync_verified: bool = False
    human_approved: bool = False
    rights: str = RIGHTS
    publication: str = PUBLICATION
    auto_post: bool = AUTO_POST

def team_totals(rows=ROWS):
    return {t: sum(amount for _, team, amount in rows if team == t)
            for t in ("A", "B")}

def stage_at(second):
    if not 0 <= second < 20:
        raise ValueError("outside storyboard")
    return next(stage for start, end, stage in SCENES
                if start <= second < end)

def validate_proof(rows=ROWS):
    if len(rows) != 6 or len({(d, team) for d, team, _ in rows}) != 6:
        raise ValueError("rows must be six unique synthetic entries")
    totals = team_totals(rows)
    if totals != {"A": 35, "B": 26}:
        raise ValueError("visible totals must match synthetic source")
    if sum(totals.values()) != sum(v for _, _, v in rows):
        raise ValueError("comparison total mismatch")
    if SCENES[0][0] != 0 or SCENES[-1][1] != 20:
        raise ValueError("invalid storyboard")
    if any(SCENES[i][1] != SCENES[i + 1][0] for i in range(len(SCENES)-1)):
        raise ValueError("timeline gap")
    return totals

def release_gate(state: QualityState):
    if state.auto_post or state.publication != PUBLICATION:
        raise ValueError("never auto-post or mark published in this review")
    if state.rights != RIGHTS:
        raise ValueError("rights provenance missing")
    if not state.japanese_voice_verified:
        return "REVIEW_ONLY_NARRATION_MISSING"
    if not state.semantic_caption_sync_verified:
        return "REVIEW_ONLY_SYNC_UNVERIFIED"
    return "HUMAN_REVIEW_REQUIRED"
