"""Reusable fail-closed motion / evidence contract for ten genres.
No claim about narration language or quality is made from AAC presence.
"""
from dataclasses import dataclass
from math import ceil, isfinite

ALLOWED_GENRES = frozenset({'ai_productivity','miniature','before_after','business','science','history','food','travel','lifestyle','gadgets'})

@dataclass(frozen=True)
class MotionShot:
    genre: str
    start: float
    end: float
    stages: int
    source: str = 'SYNTHETIC_LOCAL'
    caption: str = ''

def validate_motion(shots, duration, publication='NOT_APPROVED', auto_post=False):
    if publication != 'NOT_APPROVED' or auto_post:
        raise ValueError('publication requires human approval; automatic posting prohibited')
    if not isfinite(duration) or duration <= 0 or not shots:
        raise ValueError('duration/shots missing')
    last = 0.0
    for s in shots:
        if s.genre not in ALLOWED_GENRES: raise ValueError('unknown genre')
        if s.source != 'SYNTHETIC_LOCAL': raise ValueError('rights not approved')
        if not all(isfinite(v) for v in (s.start,s.end)): raise ValueError('nonfinite time')
        if not 0 <= last <= s.start < s.end <= duration + 0.04:
            raise ValueError('shot timing overlap or out of range')
        if s.stages < 2: raise ValueError('static shot without change')
        if not s.caption or len(s.caption) > 80: raise ValueError('caption missing/too long')
        last = s.end
    return {'shots':len(shots),'stages':sum(s.stages for s in shots),'rights':'SYNTHETIC_LOCAL',
            'narration':'UNVERIFIED','semantic_sync':'UNVERIFIED','publication':'NOT_APPROVED'}

def reveal_count(duration, fps=4):
    if not isfinite(duration) or duration<=0 or fps<=0: raise ValueError('bad reveal parameters')
    return ceil(duration*fps)

def text_prefix(text, fraction):
    if not 0 <= fraction <= 1: raise ValueError('bad fraction')
    return text[:int(round(len(text)*fraction))]
