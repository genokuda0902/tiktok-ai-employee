"""Review-only reusable attention cues. No media upload or publication."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

FRAME_WIDTH, FRAME_HEIGHT = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 200, 1510
ALLOWED_RIGHTS = {'USER_OWNED_REVIEW_ONLY', 'ORIGINAL_SYNTHETIC_REVIEW_ONLY'}

@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    box: tuple[int, int, int, int]
    focus: str
    genre: str = 'ai_work'

def validate_cues(cues: Iterable[Cue], duration: float, rights: str,
                  publication: str = 'NOT_APPROVED') -> tuple[Cue, ...]:
    if rights not in ALLOWED_RIGHTS:
        raise ValueError('Missing review-only rights approval; fail closed')
    if publication != 'NOT_APPROVED':
        raise ValueError('Review overlays must not approve or publish')
    if not 0 < duration <= 120:
        raise ValueError('Invalid duration')
    checked = tuple(cues)
    if not checked:
        raise ValueError('At least one cue required')
    last_start = -1.0
    for cue in checked:
        if not (0 <= cue.start < cue.end <= duration):
            raise ValueError('Invalid cue time')
        if cue.start < last_start:
            raise ValueError('Cues must be sorted')
        last_start = cue.start
        x0,y0,x1,y1 = cue.box
        if not (40 <= x0 < x1 <= FRAME_WIDTH-40 and
                SAFE_TOP <= y0 < y1 <= SAFE_BOTTOM):
            raise ValueError('Focus box outside safe visual region')
        if not cue.focus.strip() or not cue.genre.strip():
            raise ValueError('Missing semantic focus/genre')
    return checked

def active_cue(cues: Iterable[Cue], time_s: float) -> Cue | None:
    return next((cue for cue in cues if cue.start <= time_s < cue.end), None)

def pulse(time_s: float, start: float) -> float:
    import math
    elapsed = max(0.0, time_s-start)
    return 0.5 + 0.5*math.sin(elapsed*math.pi*2*1.25)

def draw_overlay(frame, cue: Cue | None, time_s: float):
    if cue is None:
        return frame
    import cv2
    import numpy as np
    x0,y0,x1,y1=cue.box
    v=pulse(time_s,cue.start)
    color=(int(148+40*v),int(210+25*v),int(56+20*v))
    length=52
    for x,dx in ((x0,1),(x1,-1)):
        for y,dy in ((y0,1),(y1,-1)):
            cv2.line(frame,(x,y),(x+dx*length,y),color,5,cv2.LINE_AA)
            cv2.line(frame,(x,y),(x,y+dy*length),color,5,cv2.LINE_AA)
    yy=int(y0+25+(y1-y0-50)*(0.5-0.5*np.cos(min(1,(time_s-cue.start)/(cue.end-cue.start))*np.pi)))
    cx=x0-19
    cv2.circle(frame,(cx,yy),11,color,-1,cv2.LINE_AA)
    cv2.circle(frame,(cx,yy),15,(250,250,250),2,cv2.LINE_AA)
    return frame
