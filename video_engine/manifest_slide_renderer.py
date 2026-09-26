"""Manifest-driven 8-12 image slide render plan (zero-cost, manual-post only)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Scene:
    image: str
    duration: float
    motion: str

ALLOWED_MOTION={"push_in","pull_out"}

def validate_scenes(scenes: Sequence[Scene], width=1080, height=1920, fps=30) -> bool:
    if (width,height,fps)!=(1080,1920,30):
        raise ValueError("delivery must be 1080x1920@30")
    if not 8 <= len(scenes) <= 12:
        raise ValueError("renderer requires 8-12 scenes")
    total=0.0
    for i,s in enumerate(scenes):
        if not s.image.strip():
            raise ValueError(f"scene {i} missing image")
        if not 0.8 <= s.duration <= 4.0:
            raise ValueError(f"scene {i} duration outside readable range")
        if s.motion not in ALLOWED_MOTION:
            raise ValueError(f"scene {i} unsupported motion")
        total += s.duration
    if not 8.0 <= total <= 35.0:
        raise ValueError("total duration outside short-form range")
    return True

def release_contract() -> dict:
    return {"zero_cost":True,"manifest_driven":True,"cuts_min":8,"cuts_max":12,
            "preserve_japanese_audio":True,"preserve_burned_captions":True,
            "human_approval_required":True,"manual_post_only":True,"auto_post":False}
