"""Zero-cost semantic pacing contract for image-first TikTok slides.

This module does not post or publish. It only validates a reusable timing plan
for an eight-beat vertical storyboard. Human rights/quality approval remains
mandatory.
"""

DEFAULT_BEATS = (
    ("hook", 1.20),
    ("before", 1.45),
    ("instruction", 1.65),
    ("processing", 1.50),
    ("verification", 1.50),
    ("before_after", 2.00),
    ("application", 1.45),
    ("cta", 1.95),
)


def semantic_pacing(beats=DEFAULT_BEATS, *, width=1080, height=1920):
    if (width, height) != (1080, 1920):
        raise ValueError("portrait delivery must be 1080x1920")
    if len(beats) != 8:
        raise ValueError("eight semantic beats required")
    names = [name for name, _ in beats]
    if len(names) != len(set(names)):
        raise ValueError("semantic beat names must be unique")
    durations = [float(seconds) for _, seconds in beats]
    if any(seconds < 1.0 or seconds > 2.2 for seconds in durations):
        raise ValueError("each beat must remain readable without stalling")
    total = round(sum(durations), 3)
    if not 12.0 <= total <= 15.0:
        raise ValueError("short-form pacing total must remain 12-15 seconds")
    return {"beats": tuple(beats), "duration": total, "width": width, "height": height}


def release_policy():
    return {
        "zero_cost": True,
        "image_first": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "rights_approval_required": True,
        "narration_semantic_sync_must_be_verified_separately": True,
    }
