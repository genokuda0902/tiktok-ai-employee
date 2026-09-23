"""Zero-cost semantic scene-entry emphasis for image-first TikTok renders.

Adds a short, bounded scale settle at meaning boundaries so image changes read as
intentional edits without stacking global filters.  Release remains manual-only.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class EntryPunch:
    start: float
    duration: float = 0.24
    scale_from: float = 1.018

    def validate(self, video_duration: float) -> None:
        if not 0 <= self.start < video_duration:
            raise ValueError("scene start outside video")
        if not 0.12 <= self.duration <= 0.35:
            raise ValueError("entry punch duration must stay subtle")
        if not 1.005 <= self.scale_from <= 1.025:
            raise ValueError("entry punch scale must stay subtle")


def build_entry_punches(scene_starts, video_duration: float):
    starts = tuple(float(v) for v in scene_starts)
    if not starts or starts[0] != 0.0:
        raise ValueError("scene timeline must begin at zero")
    if starts != tuple(sorted(set(starts))):
        raise ValueError("scene starts must be unique and increasing")
    punches = tuple(EntryPunch(start=s) for s in starts)
    for punch in punches:
        punch.validate(video_duration)
    return punches


def render_contract(width=1080, height=1920):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery must be 1080x1920")
    return {
        "zero_cost": True,
        "semantic_boundaries_only": True,
        "preserve_narration": True,
        "preserve_caption_copy": True,
        "rights_check_required": True,
        "human_approval_required": True,
        "auto_post": False,
    }
