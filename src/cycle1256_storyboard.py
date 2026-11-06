"""Cycle1256 reusable counter storyboard and caption timeline. Review only."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    label: str
    caption: str

SCENES = (
    Scene(0, 5, "BEFORE", "毎回、数字を足していた"),
    Scene(5, 10, "ACTION", "計算式を入力"),
    Scene(10, 15, "AFTER", "合計がすぐ出る"),
)

def counter_value(t: float, target: int = 300) -> int:
    """Animate the last scene from 0 to target during its first 1.2 s."""
    if t < 10:
        return 0
    return round(target * min(1, max(0, (t - 10) / 1.2)))

def validate_scenes(scenes=SCENES, duration=15.0):
    assert scenes and scenes[0].start == 0
    assert all(s.caption and s.end > s.start for s in scenes)
    assert all(a.end == b.start for a,b in zip(scenes, scenes[1:]))
    assert scenes[-1].end == duration

def srt(scenes=SCENES):
    def ts(x):
        ms=round(x*1000)
        return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
    return "\n".join(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.caption}\n" for i,s in enumerate(scenes,1))
