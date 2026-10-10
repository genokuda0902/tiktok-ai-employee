"""Cycle466: reusable genre-neutral safety and timeline contract. Review only."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    stage: str
    title: str
    caption: str
    narration: str
    visual: str

def validate(scenes, manifest, duration=20.0):
    if not 6 <= len(scenes) <= 12:
        raise ValueError("scene count")
    if scenes[0].start != 0 or scenes[0].end > 1.5:
        raise ValueError("hook")
    if abs(scenes[-1].end-duration)>1e-6:
        raise ValueError("duration")
    for i,s in enumerate(scenes):
        if s.end<=s.start or s.end-s.start>5:
            raise ValueError("scene length")
        if not all((s.stage,s.title,s.caption,s.narration,s.visual)):
            raise ValueError("missing scene content")
        if i and abs(s.start-scenes[i-1].end)>1e-6:
            raise ValueError("timeline discontinuity")
    if manifest.get("asset_rights")!="ORIGINAL_SYNTHETIC":
        raise ValueError("rights unverified")
    if manifest.get("privacy")!="NO_REAL_PERSONAL_DATA":
        raise ValueError("privacy unverified")
    if manifest.get("publication")!="NOT_APPROVED" or manifest.get("auto_post") is not False:
        raise ValueError("publishing forbidden")
    if manifest.get("narration_status")!="VERIFIED_JAPANESE" and manifest.get("quality_status")!="HUMAN_REVIEW":
        raise ValueError("missing voice requires human review")
    return True

def caption_bounds_ok(box, width=720, height=1280):
    x0,y0,x1,y1=box
    return 36<=x0<x1<=width-36 and 180<=y0<y1<=height-160

def publication_allowed(manifest):
    return all((manifest.get("publication")=="APPROVED",
        manifest.get("human_approval") is True,
        manifest.get("narration_status")=="VERIFIED_JAPANESE",
        manifest.get("asset_rights")=="ORIGINAL_SYNTHETIC",
        manifest.get("privacy")=="NO_REAL_PERSONAL_DATA",
        manifest.get("auto_post") is False))
