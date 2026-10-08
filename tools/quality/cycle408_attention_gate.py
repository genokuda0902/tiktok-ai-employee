"""Cycle408: reusable focus-sequence contract for 9:16 image-slide videos.
Never claims voice exists when the source AAC track is silent.
No network, paid services, third-party assets or posting actions.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class FocusStep:
    start: float
    end: float
    box: tuple[int, int, int, int]
    label: str

def validate_focus_steps(steps, *, width=1080, height=1920, duration=16.42):
    """Validate timed attention boxes before applying drawbox overlays."""
    if not steps:
        raise ValueError("focus steps required")
    prev_start = -1.0
    for step in steps:
        x, y, w, h = step.box
        if not (0 <= step.start < step.end <= duration):
            raise ValueError("invalid time window")
        if not (0 <= x and 0 <= y and w > 0 and h > 0 and x+w <= width and y+h <= 1160):
            raise ValueError("focus overlay must not enter caption / UI region")
        if step.start < prev_start:
            raise ValueError("steps must be ordered")
        prev_start = step.start
    return True

def ffmpeg_filters(steps):
    validate_focus_steps(steps)
    return ",".join(
        f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0xA7F6C9@0.82:t=5:enable='between(t,{s.start:.2f},{s.end:.2f})'"
        for s in steps for x,y,w,h in [s.box]
    ) + ",format=yuv420p"

def voice_status(*, voice_engine_found, verified_nonzero_audio, human_listening_verified):
    if not voice_engine_found or not verified_nonzero_audio:
        return "SILENT_VISUAL_PREVIEW_ONLY"
    if not human_listening_verified:
        return "VOICE_PRESENT_HUMAN_REVIEW_REQUIRED"
    return "VOICE_LISTENING_REVIEWED"
