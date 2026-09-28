"""Bridge a rights-cleared six-image manifest into the semantic timeline.

This module is intentionally renderer-agnostic. It fails closed unless every semantic
beat has one distinct approved image, and it returns a single source of truth that a
renderer can use for image timing, Japanese narration timing and caption timing.
It never publishes to TikTok.
"""
from dataclasses import dataclass
from .scene_asset_manifest import SceneAsset, REQUIRED_BEATS, validate_manifest
from .semantic_timeline import Scene, build_timeline


@dataclass(frozen=True)
class SceneCopy:
    beat: str
    narration: str
    caption: str
    duration_s: float


def build_asset_timeline(assets: list[SceneAsset], copy: list[SceneCopy]) -> list[dict]:
    """Return one validated timeline joining six approved images to six semantic beats."""
    validate_manifest(assets)
    if len(copy) != len(REQUIRED_BEATS):
        raise ValueError("exactly six semantic copy entries are required")
    if tuple(c.beat for c in copy) != REQUIRED_BEATS:
        raise ValueError("copy must follow hook/problem/solution/demo/result/cta order")

    scenes = [
        Scene(
            image=asset.image_path,
            narration=text.narration,
            caption=text.caption,
            duration_s=text.duration_s,
        )
        for asset, text in zip(assets, copy)
    ]
    timeline = build_timeline(scenes)
    for row, beat in zip(timeline, REQUIRED_BEATS):
        row["beat"] = beat
        row["rights_status"] = assets[row["scene"] - 1].rights_status
        row["approved"] = True
    return timeline


def delivery_policy() -> dict:
    return {
        "zero_cost": True,
        "distinct_images_required": 6,
        "human_quality_review_required": True,
        "human_rights_review_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
