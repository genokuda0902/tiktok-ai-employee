"""Reusable TikTok scene-contract validator.

Fail-closed quality guard for image-first review videos.
No publication action is performed here.
"""

ALLOWED_ROLES = ("HOOK", "PAIN", "SOLUTION", "PROOF", "VALUE", "CTA")

def validate_scene_plan(plan):
    errors = []
    scenes = plan.get("scenes") or []
    duration = plan.get("target_seconds")

    if not isinstance(duration, (int, float)) or not 15 <= duration <= 25:
        errors.append("target_seconds must be 15..25")

    if not scenes:
        errors.append("scenes required")
        return errors

    roles = [s.get("role") for s in scenes]
    if roles[0] != "HOOK":
        errors.append("first scene must be HOOK")
    if "PROOF" not in roles:
        errors.append("PROOF scene required")
    if roles[-1] != "CTA":
        errors.append("last scene must be CTA")

    for i, scene in enumerate(scenes):
        role = scene.get("role")
        if role not in ALLOWED_ROLES:
            errors.append(f"scene {i}: invalid role")
        seconds = scene.get("seconds")
        if not isinstance(seconds, (int, float)) or seconds <= 0 or seconds > 5:
            errors.append(f"scene {i}: seconds must be >0 and <=5")
        if not scene.get("visual_change"):
            errors.append(f"scene {i}: visual_change required")
        if not scene.get("purpose"):
            errors.append(f"scene {i}: purpose required")
        if not scene.get("asset_approved", False):
            errors.append(f"scene {i}: approved asset required")

    hook_seconds = scenes[0].get("seconds", 99)
    # The hook is a cumulative timing gate, not just a per-scene duration check.
    # This also fails closed when a malformed/negative duration slips in.
    if not isinstance(hook_seconds, (int, float)) or hook_seconds <= 0 or hook_seconds > 1.5:
        errors.append("HOOK must finish within 1.5 seconds")

    if plan.get("publication_gate") != "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED":
        errors.append("publication gate must remain fail-closed")
    return errors
