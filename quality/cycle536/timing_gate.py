"""Cycle 536 generic scene timing and safe-area validation."""
FPS=30
START=6.0
END=8.5

def validate_timeline(start=START,end=END,fps=FPS):
    if start<0 or end<=start or fps!=30:
        raise ValueError('invalid scene timing')
    if end>20.0:
        raise ValueError('outside video duration')
    return round((end-start)*fps)

def validate_safe_rect(rect):
    x0,y0,x1,y1=rect
    return 48<=x0<x1<=1032 and 48<=y0<y1<=1680
