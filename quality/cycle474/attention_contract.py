"""Genre-independent visual attention contract for review-only TikTok previews.

The scene planner and renderer can use this for 10 genres. It does not certify
spoken Japanese or grant publishing permission.
"""
from __future__ import annotations

BAD_STAGES = {"PRIVATE_ASSET", "UNLICENSED_ASSET"}


def attention_phase(t: float, start: float, end: float) -> str:
    """Return deterministic beat phases for a scene; no synthetic QA claims."""
    if end <= start or not start <= t < end:
        raise ValueError("timestamp outside scene")
    u = (t - start) / (end - start)
    return "reveal" if u < .22 else "proof" if u < .78 else "recap"


def pointer_allowed(stage: str, phase: str) -> bool:
    """Pointer motion is meaningful only for on-screen interaction."""
    return stage in {"SOURCE", "RETRY"} and phase != "recap"


def validate_attention_plan(plan: dict) -> dict:
    scenes = plan.get("scenes", [])
    if not scenes:
        raise ValueError("no scenes")
    if scenes[0]["start"] != 0 or scenes[0]["end"] > 1.5:
        raise ValueError("first proof hook must fit in 1.5 seconds")
    for a, b in zip(scenes, scenes[1:]):
        if abs(float(a["end"]) - float(b["start"])) > .0001:
            raise ValueError("timeline gap/overlap")
    if abs(float(scenes[-1]["end"]) - float(plan.get("duration", -1))) > .0001:
        raise ValueError("duration mismatch")
    if any(s.get("stage") in BAD_STAGES for s in scenes):
        raise ValueError("unapproved assets")
    if any(not s.get("caption", "").strip() for s in scenes):
        raise ValueError("missing captions")
    if plan.get("auto_post") or plan.get("publication") != "NOT_APPROVED":
        raise ValueError("publication must fail closed")
    if plan.get("narration_status") != "NOT_GENERATED":
        raise ValueError("narration cannot be attested by this visual-only gate")
    return {"scenes": len(scenes), "status": "REVIEW_ONLY", "voice": "NOT_VERIFIED"}
