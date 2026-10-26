"""Frame-exact, genre-agnostic UI state timeline for offline TikTok image-slide videos.

Only simulated interface states; no real apps, credentials, personal data or posting.
Use a single narration and a single non-overlapping caption track.
"""
from __future__ import annotations
from dataclasses import dataclass

W, H, FPS, TOTAL_FRAMES = 1080, 1920, 30, 691
CAPTION_TOP = 1438
GENRES = (
    'ai_productivity','beauty','romance_psychology','money_saving',
    'sales_business','career','health_lifestyle','trivia_science',
    'travel_food','product_lifestyle',
)

@dataclass(frozen=True)
class State:
    scene: int
    stage: int
    start: int
    end: int

SCENE_STATES = (
    ((0,24),(24,56),(56,93)),
    ((93,118),(118,145),(145,176)),
    ((176,254),),
    ((254,272),(272,296),(296,318),(318,341)),
    ((341,363),(363,384),(384,405),(405,426)),
    ((426,518),),
    ((518,550),(550,573),(573,596)),
    ((596,691),),
)

def build_timeline():
    return tuple(State(scene=i,stage=j,start=a,end=b)
                 for i,states in enumerate(SCENE_STATES,1)
                 for j,(a,b) in enumerate(states))

def validate_timeline(timeline=None, genre='ai_productivity'):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    timeline=build_timeline() if timeline is None else tuple(timeline)
    if not timeline or timeline[0].start!=0 or timeline[-1].end!=TOTAL_FRAMES:
        raise ValueError('timeline must cover entire video')
    for i,s in enumerate(timeline):
        if not (1<=s.scene<=8 and 0<=s.stage<6 and 0<=s.start<s.end<=TOTAL_FRAMES):
            raise ValueError('invalid state')
        if i and (timeline[i-1].end!=s.start or s.scene<timeline[i-1].scene):
            raise ValueError('gap, overlap, or scene reversal')
        if i and s.scene==timeline[i-1].scene and s.stage!=timeline[i-1].stage+1:
            raise ValueError('state numbering not consecutive')
        if i and s.scene>timeline[i-1].scene and s.stage!=0:
            raise ValueError('scene must start with stage zero')
    if len(set(s.scene for s in timeline))!=8:
        raise ValueError('expected eight scenes')
    if not any(sum(x.scene==scene for x in timeline)>1 for scene in range(1,9)):
        raise ValueError('must animate at least one scene')
    return True

def frame_to_seconds(frame):
    if not 0<=frame<=TOTAL_FRAMES:
        raise ValueError('frame out of range')
    return frame/FPS

HIT_TARGETS={'prompt_send':(742,1192,945,1268),'template_save':(545,1152,941,1230)}
def validate_hit_targets(targets=HIT_TARGETS):
    for key,box in targets.items():
        x0,y0,x1,y1=box
        if not (40<=x0<x1<=W-40 and 160<=y0<y1<=CAPTION_TOP-60):
            raise ValueError('unsafe interactive target: '+key)
    return True
