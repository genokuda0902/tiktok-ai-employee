"""Reusable zero-cost ten-genre motion-safe layout for 9:16 editorial videos."""
from dataclasses import dataclass
from quality_core import W,H,CAPTION_TOP,GENRES,Rect
SCALED_W,SCALED_H=1120,1992
CROP_W,CROP_H=W,H
PAN_X_CENTER,PAN_X_AMPLITUDE=20,15
PAN_Y_CENTER,PAN_Y_AMPLITUDE=36,23
@dataclass(frozen=True)
class FocusCue:
    start:float
    end:float
    box:tuple[int,int,int,int]
    label:str
FOCUS_CUES=(FocusCue(11.65,14.0,(126,1085,820,1265),'computed_completion'),)
def validate_motion(genre='ai_productivity',cues=FOCUS_CUES):
    if genre not in GENRES:raise ValueError('Unknown genre')
    if SCALED_W<W or SCALED_H<H:raise ValueError('Overscan required')
    if PAN_X_CENTER-PAN_X_AMPLITUDE<0 or PAN_X_CENTER+PAN_X_AMPLITUDE>SCALED_W-W:raise ValueError('X pan clips')
    if PAN_Y_CENTER-PAN_Y_AMPLITUDE<0 or PAN_Y_CENTER+PAN_Y_AMPLITUDE>SCALED_H-H:raise ValueError('Y pan clips')
    for c in cues:
        if not 0<=c.start<c.end<=23.04:raise ValueError('Invalid focus timing')
        if not Rect(0,0,W,CAPTION_TOP).contains(Rect(*c.box)):raise ValueError('Focus collides with caption')
        if c.box[2]-c.box[0]<10 or c.box[3]-c.box[1]<10:raise ValueError('Cue too small')
    return True
def base_motion_filter():
    validate_motion()
    return (f'fps=30,scale={SCALED_W}:{SCALED_H}:flags=lanczos,'
            f"crop={W}:{H}:x='{PAN_X_CENTER}+{PAN_X_AMPLITUDE}*sin(n/17)':"
            f"y='{PAN_Y_CENTER}+{PAN_Y_AMPLITUDE}*cos(n/21)',format=yuv420p")
def focus_filters():
    validate_motion()
    result=[]
    for c in FOCUS_CUES:
        x0,y0,x1,y1=c.box
        result.append(f"drawbox=x={x0}:y={y0}:w={x1-x0}:h={y1-y0}:color=0xFFD966@0.92:t=7:enable='between(t,{c.start},{c.end})'")
    return ','.join(result)
