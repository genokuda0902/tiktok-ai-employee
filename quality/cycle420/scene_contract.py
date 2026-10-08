"""Fail-closed review scene contract shared by all ten genres."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Scene:
    scene_id: str
    caption: str
    narration: str
    duration: float

class ContractError(ValueError): pass

def validate(scenes, *, rights, publication, auto_post=False):
    if rights != "ORIGINAL_PROCEDURAL" or publication != "NOT_APPROVED" or auto_post:
        raise ContractError("rights or publication not approved")
    if not 6 <= len(scenes) <= 10:
        raise ContractError("scene count")
    if len({s.scene_id for s in scenes}) != len(scenes):
        raise ContractError("duplicate scene")
    if abs(sum(s.duration for s in scenes)-20) > 1/30:
        raise ContractError("timeline")
    for s in scenes:
        if not s.caption or not s.narration or len(s.caption)>22:
            raise ContractError("missing or oversized caption/voice")
    return True

def verify_voice(durations, *, engine, segments):
    if engine != "OPEN_JTALK_LOCAL" or len(durations)!=len(segments):
        raise ContractError("missing Japanese TTS provenance")
    if any(not 0.2 < d < s.duration-0.1 for d,s in zip(durations,segments)):
        raise ContractError("narration duration outside scene")
    return True
