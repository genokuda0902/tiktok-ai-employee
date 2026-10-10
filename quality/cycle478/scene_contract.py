"""Reusable, genre-neutral TikTok scene plan and publication safety checks.

Technical validation is not Japanese voice verification or human approval.
"""
from __future__ import annotations

REQUIRED = {
    "rights": "ORIGINAL_SYNTHETIC",
    "privacy": "NO_PERSONAL_DATA",
    "publication": "NOT_APPROVED",
    "human_approval": False,
    "auto_post": False,
    "reference_equivalence": False,
}

class SceneContractError(ValueError):
    pass

def validate(plan):
    errors = []
    for key, expected in REQUIRED.items():
        if plan.get(key) != expected:
            errors.append(f"{key}: unsafe or unverified")
    scenes = plan.get("scenes") or []
    duration = float(plan.get("duration", 0))
    if not 15 <= duration <= 25:
        errors.append("duration outside 15-25s")
    if not 5 <= len(scenes) <= 10:
        errors.append("scene count outside 5-10")
    cursor = 0.0
    for i, scene in enumerate(scenes):
        start, end = float(scene.get("start", -1)), float(scene.get("end", -1))
        if abs(start - cursor) > 0.04 or end <= start:
            errors.append(f"scene {i}: gap/overlap/nonpositive")
        if not scene.get("caption") or not scene.get("kind"):
            errors.append(f"scene {i}: missing caption or kind")
        if len(scene.get("caption", "")) > 40:
            errors.append(f"scene {i}: caption too long")
        cursor = end
    if abs(cursor - duration) > 0.04:
        errors.append("duration does not match scene timeline")
    if scenes and float(scenes[0].get("end", 99)) > 1.5:
        errors.append("hook longer than 1.5s")
    return errors

def release_errors(plan, voice_verified=False, captions_speech_aligned=False):
    errors = validate(plan)
    if not voice_verified or plan.get("narration_status") != "GENERATED_AND_VERIFIED":
        errors.append("Japanese narration not verified")
    if not captions_speech_aligned or plan.get("subtitle_provenance") != "MEASURED_SPEECH_TIMELINE":
        errors.append("Japanese speech/caption sync not verified")
    # Technical success never grants publication permission.
    if not plan.get("human_approval"):
        errors.append("human approval required")
    return errors
