"""Zero-cost manifest timeline planner for the image-first TikTok renderer.

Reimplementation only: validates StoryManifest and turns it into deterministic
cut boundaries/motion assignments. Rendering/publishing remain separate.
"""
from dataclasses import dataclass
from typing import Tuple
from video_engine.unified_story_manifest import StoryManifest

@dataclass(frozen=True)
class PlannedCut:
    index: int
    start: float
    end: float
    duration: float
    motion: str

def plan_timeline(manifest: StoryManifest) -> Tuple[PlannedCut, ...]:
    manifest.validate()
    cursor = 0.0
    out = []
    motions = ("zoom_in", "zoom_out", "pan_left", "pan_right")
    for i, cut in enumerate(manifest.cuts):
        start = round(cursor, 3)
        end = round(start + cut.duration, 3)
        out.append(PlannedCut(i, start, end, cut.duration, motions[i % len(motions)]))
        cursor = end
    if abs(cursor - manifest.duration) > 0.002:
        raise ValueError("timeline duration drift")
    return tuple(out)

def release_contract() -> dict:
    return {
        "zero_cost": True,
        "single_source_manifest": True,
        "human_approval_required": True,
        "manual_post_only": True,
        "auto_post": False,
    }
