"""Reusable scene-plan schema for ten categories. Review-only output."""
GENRES = ("ai_work", "beauty", "relationships", "budget", "sales",
          "career", "wellness", "science", "travel", "shopping")
FIELDS = ("audience", "goal", "constraints")
def validate_plan(plan):
    if plan.get("genre") not in GENRES:
        raise ValueError("unknown genre")
    if any(not isinstance(plan.get(key), str) or not plan[key].strip() for key in FIELDS):
        raise ValueError("missing scene field")
    return True
def require_narration_approval(native_japanese, human_approved):
    if not native_japanese or not human_approved:
        raise ValueError("Japanese narration not approved")
    return True
