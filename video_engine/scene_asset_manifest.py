"""Fail-closed asset manifest for the zero-cost image-slide route.

Each semantic beat must resolve to its own approved image asset before rendering.
This is genre-independent and deliberately does not publish or fetch paid media.
"""
from dataclasses import dataclass

REQUIRED_BEATS = ("hook", "problem", "solution", "demo", "result", "cta")

@dataclass(frozen=True)
class SceneAsset:
    beat: str
    image_path: str
    rights_status: str
    approved: bool


def validate_manifest(assets: list[SceneAsset]) -> dict:
    if len(assets) != len(REQUIRED_BEATS):
        raise ValueError("exactly six semantic assets are required")
    beats = tuple(a.beat for a in assets)
    if beats != REQUIRED_BEATS:
        raise ValueError("assets must follow hook/problem/solution/demo/result/cta order")
    paths = [a.image_path.strip() for a in assets]
    if any(not p for p in paths) or len(set(paths)) != len(paths):
        raise ValueError("each beat requires a distinct image asset")
    for a in assets:
        if not a.approved or a.rights_status not in {"owned", "public-safe", "licensed-free"}:
            raise ValueError(f"asset for {a.beat} is not approved/rights-cleared")
    return {
        "scene_count": 6,
        "distinct_images": 6,
        "zero_cost": True,
        "human_approval_required": True,
        "auto_post": False,
    }
