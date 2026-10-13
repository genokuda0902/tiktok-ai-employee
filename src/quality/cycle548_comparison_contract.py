"""Reusable safety and factuality gate for cycle548 comparison scenes.

Cycle548 video rendering uses the same synthetic four-value contract. This
module does not approve media for publication or claim real time savings.
"""
GENRES = (
    "ai_work", "beauty", "relationships", "finance", "sales_business",
    "career", "health_lifestyle", "science_trivia", "travel_food",
    "shopping_lifestyle",
)
STEPS = ("instruction", "formula_check", "human_review")


def validate_scene(scene):
    if scene.get("genre") not in GENRES:
        raise ValueError("unsupported genre")
    if scene.get("asset_status") != "synthetic_review_only":
        raise ValueError("media not cleared for review-only use")
    if scene.get("publication_status") != "NOT_APPROVED":
        raise ValueError("publication is not approved")
    if scene.get("data_is_real") is not False:
        raise ValueError("only synthetic data permitted")
    values = scene.get("values")
    if not isinstance(values, list) or len(values) != 4:
        raise ValueError("exactly four values required")
    if any(type(x) is not int or not 0 < x <= 9999 for x in values):
        raise ValueError("invalid value")
    if scene.get("total") != sum(values):
        raise ValueError("total mismatch")
    return True


def reveal_state(local_time):
    """Return deterministic state for a two-second progressive comparison."""
    if not isinstance(local_time, (int, float)) or not 0 <= local_time < 2:
        raise ValueError("time must be inside comparison scene")
    return {
        "visible_steps": min(3, int(local_time / .52) + 1),
        "show_total": local_time >= 1.35,
        "show_calculating": .75 <= local_time < 1.35,
        "status": "HUMAN_REVIEW",
        "publication_status": "NOT_APPROVED",
    }
