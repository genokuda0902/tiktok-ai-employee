"""Cross-genre timing contract for safe 10-scene vertical explainer videos."""
from dataclasses import dataclass

GENRES = ('ai_productivity','trivia','cooking','beauty','finance','wellness','travel','product_demo','story','business')
REVEAL_SCENES = frozenset((2,3))

@dataclass(frozen=True)
class Beat:
    scene: int
    phase: int
    t_start: float
    t_end: float

def build_beats(scene_count=10, fps=2, beats_per_scene=4, genre='ai_productivity'):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if scene_count < 4 or fps != 2 or beats_per_scene != 4:
        raise ValueError('contract requires >=4 scenes, 2fps, 4 beats')
    beats=[]
    for scene in range(scene_count):
        for phase in range(1,beats_per_scene+1):
            t=2*scene+(phase-1)*0.5
            beats.append(Beat(scene,phase,t,t+0.5))
    return beats

def build_plan(scene_count=10, fps=2, beats_per_scene=4, genre='ai_productivity'):
    return [(b.scene,b.phase if b.scene in REVEAL_SCENES else 4)
            for b in build_beats(scene_count,fps,beats_per_scene,genre)]

def validate_plan(plan, scene_count=10):
    if len(plan) != scene_count*4:
        raise ValueError('wrong frame count')
    for i,(scene,phase) in enumerate(plan):
        if scene != i//4 or phase not in range(1,5):
            raise ValueError('wrong scene/phase')
        if scene not in REVEAL_SCENES and phase != 4:
            raise ValueError('unexpected reveal outside proof scene')
    return True
