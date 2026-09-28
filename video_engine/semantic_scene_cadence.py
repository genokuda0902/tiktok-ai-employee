"""Genre-independent semantic scene cadence for image-slide TikTok videos.

Keeps visual changes tied to meaning boundaries rather than stacking global filters.
Zero-cost and manual-release only.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class SceneBeat:
    start: float
    end: float
    role: str

DEFAULT_ROLES = ("hook", "problem", "solution", "demo", "result", "cta")

def build_scene_beats(duration: float = 12.7, roles=DEFAULT_ROLES):
    if not 6.0 <= duration <= 60.0:
        raise ValueError("duration outside supported short-form range")
    if not roles or len(roles) > 12 or len(set(roles)) != len(roles):
        raise ValueError("roles must be unique and bounded")
    # Front-load cuts for hook/problem; give demo/result slightly more breathing room.
    weights = [0.12, 0.14, 0.17, 0.22, 0.20, 0.15]
    if len(roles) != 6:
        weights = [1.0 / len(roles)] * len(roles)
    total = sum(weights)
    cursor = 0.0
    beats = []
    for i, (role, weight) in enumerate(zip(roles, weights)):
        end = duration if i == len(roles)-1 else cursor + duration * weight / total
        beats.append(SceneBeat(round(cursor, 3), round(end, 3), role))
        cursor = end
    return beats

def render_contract(width=1080, height=1920):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    return {
        "zero_cost": True,
        "one_visual_asset_per_beat": True,
        "sync_narration_caption_to_beat": True,
        "human_approval_required": True,
        "auto_post": False,
        "rights_check_required": True,
    }
