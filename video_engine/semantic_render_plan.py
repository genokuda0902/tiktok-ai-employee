"""Genre-independent render plan for the zero-cost image-slide route.

Binds the six rights-cleared image assets to semantic scenes so image, Japanese
narration and caption timing come from one validated timeline. Rendering remains
human-approved and manual-post only.
"""
from dataclasses import dataclass

from video_engine.scene_asset_manifest import REQUIRED_BEATS, SceneAsset, validate_manifest
from video_engine.semantic_timeline import Scene, build_timeline, validate_scenes


@dataclass(frozen=True)
class SemanticBeat:
    beat: str
    asset: SceneAsset
    narration: str
    caption: str
    duration_s: float


def build_render_plan(beats: list[SemanticBeat]) -> list[dict]:
    if len(beats) != 6 or tuple(b.beat for b in beats) != REQUIRED_BEATS:
        raise ValueError("render plan requires hook/problem/solution/demo/result/cta")
    assets = [b.asset for b in beats]
    if any(b.beat != b.asset.beat for b in beats):
        raise ValueError("semantic beat and asset beat must match")
    validate_manifest(assets)
    scenes = [Scene(b.asset.image_path, b.narration, b.caption, b.duration_s) for b in beats]
    validate_scenes(scenes)
    timeline = build_timeline(scenes)
    for row, beat in zip(timeline, beats):
        row["beat"] = beat.beat
        row["rights_status"] = beat.asset.rights_status
        row["approved"] = beat.asset.approved
    return timeline


def release_policy() -> dict:
    return {
        "zero_cost": True,
        "width": 1080,
        "height": 1920,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
        "distinct_images_required": 6,
    }
