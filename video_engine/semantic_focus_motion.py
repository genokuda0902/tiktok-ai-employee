"""Beat-aware focus plan for image-first TikTok stories.

Keeps hook/problem/CTA wide while allowing evidence-heavy beats to use a
bounded crop/zoom. This is a reimplementation helper: zero-cost, no posting,
and human/rights approval remain mandatory.
"""

WIDE_BEATS = {"hook", "problem", "cta"}
EVIDENCE_BEATS = {"setup", "demo", "process", "result", "before", "after", "apply"}

def focus_scale(beat: str) -> float:
    key = beat.strip().lower()
    if key in WIDE_BEATS:
        return 1.0
    if key in {"demo", "result", "after"}:
        return 1.08
    if key in EVIDENCE_BEATS:
        return 1.04
    raise ValueError("unsupported story beat")

def validate_focus_plan(beats, width=1080, height=1920):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    beats = tuple(beats)
    if not 8 <= len(beats) <= 12:
        raise ValueError("story requires 8-12 beats")
    scales = tuple(focus_scale(b) for b in beats)
    if max(scales) > 1.08:
        raise ValueError("focus zoom must remain subtle")
    return scales

def release_contract():
    return {
        "zero_cost": True,
        "preserve_audio_copy": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "rights_check_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
