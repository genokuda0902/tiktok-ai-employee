"""Duration integrity guard for reusable 10-genre TikTok scene plans.

Fail closed when declared scene durations drift from target_seconds.
This module performs validation only; it never publishes content.
"""

def validate_duration_integrity(plan, tolerance=0.05):
    errors = []
    target = plan.get("target_seconds")
    scenes = plan.get("scenes") or []
    if not isinstance(target, (int, float)) or target <= 0:
        return ["target_seconds must be positive numeric"]
    if not scenes:
        return ["scenes required"]
    durations = [scene.get("seconds") for scene in scenes]
    if not all(isinstance(v, (int, float)) and v > 0 for v in durations):
        return ["all scene seconds must be positive numeric"]
    actual = sum(durations)
    if abs(actual - target) > tolerance:
        errors.append(f"scene duration sum {actual:.3f}s does not match target {target:.3f}s")
    return errors
