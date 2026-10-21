"""Pure end-card state and safe-area definitions for 10 TikTok genres."""
from pathlib import Path
import json
FPS=30
WIDTH=1080
HEIGHT=1920
SCENE_START=379
FRAME_COUNT=429
ENDCARD_RECT=(56,565,898,1103)
BLACK_FRAME_INDICES=(57,118,177,240,280,327,375)
def load_genres(path):
    obj=json.loads(Path(path).read_text(encoding="utf-8"))
    genres=obj["genres"]
    if len(genres)!=10:
        raise ValueError("Exactly ten genres required")
    for name,steps in genres.items():
        if len(steps)!=3 or any(len(step)!=2 for step in steps):
            raise ValueError("Three title/subtitle pairs required: "+name)
    return genres
def stage_at(frame):
    if frame<SCENE_START or frame>=FRAME_COUNT:
        raise ValueError("Frame outside end card")
    return 1 if frame<395 else 2 if frame<411 else 3
def inside_safe_area(rect=ENDCARD_RECT):
    x0,y0,x1,y1=rect
    return 0<=x0<x1<=WIDTH and 200<=y0<y1<=1200
