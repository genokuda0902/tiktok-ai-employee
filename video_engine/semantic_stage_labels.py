"""Genre-independent semantic stage labels for image-slide videos.

Adds a small top-safe-area label (HOOK/problem/solution/demo/CTA) derived from
semantic timeline intervals. This is presentation metadata only: it must not
change narration/caption timing or enable automatic posting.
"""
from dataclasses import dataclass

ALLOWED_STAGES = ("HOOK", "課題", "解決", "実演", "CTA")

@dataclass(frozen=True)
class Stage:
    label: str
    start_s: float
    end_s: float


def validate_stages(stages: list[Stage], duration_s: float) -> None:
    if not stages or duration_s <= 0:
        raise ValueError("stages and positive duration are required")
    cursor = 0.0
    for i, stage in enumerate(stages):
        if stage.label not in ALLOWED_STAGES:
            raise ValueError(f"unsupported stage label at {i}")
        if abs(stage.start_s - cursor) > 0.01 or stage.end_s <= stage.start_s:
            raise ValueError(f"stage {i} must be contiguous and positive")
        cursor = stage.end_s
    if abs(cursor - duration_s) > 0.05:
        raise ValueError("stage timeline must cover the full video")


def ffmpeg_overlay_filters(stages: list[Stage], duration_s: float, fontfile: str) -> str:
    validate_stages(stages, duration_s)
    filters = []
    for s in stages:
        enable = f"between(t,{s.start_s:.3f},{s.end_s:.3f})"
        filters.append(f"drawbox=x=48:y=92:w=230:h=62:color=black@0.58:t=fill:enable='{enable}'")
        filters.append(f"drawtext=fontfile='{fontfile}':text='{s.label}':fontsize=34:fontcolor=white:x=76:y=104:enable='{enable}'")
    return ",".join(filters)


def posting_policy() -> dict:
    return {"zero_cost": True, "human_approval_required": True, "auto_post": False}
