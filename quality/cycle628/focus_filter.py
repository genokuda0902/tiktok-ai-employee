"""Reusable FFmpeg filter construction for cycle628 subject-focus cues."""
import json
from pathlib import Path

CONFIG=Path(__file__).with_name("focus_config.json")

def load_config():
    cfg=json.loads(CONFIG.read_text(encoding="utf-8"))
    bounds=cfg["frame_boundaries"]
    boxes=cfg["focus_regions"]
    assert len(bounds)==9 and len(boxes)==8
    assert bounds[0]==0 and bounds[-1]==468
    assert all(a<b for a,b in zip(bounds,bounds[1:]))
    assert all(55<=x and x+w<=1025 and 408<=y and y+h<=1220 for x,y,w,h in boxes)
    assert cfg["publication"]=="NOT_APPROVED"
    return cfg

def build_filter():
    cfg=load_config()
    out=[]
    b=cfg["frame_boundaries"]
    for i,(x,y,w,h) in enumerate(cfg["focus_regions"]):
        start=b[i]+min(15,(b[i+1]-b[i])//3)
        end=b[i+1]-10
        out.append("drawbox=x=%d:y=%d:w=%d:h=%d:color=0x55ebc8@0.88:t=5:enable='between(n,%d,%d)'"%(x,y,w,h,start,end))
        out.append("drawbox=x=%d:y=%d:w=%d:h=%d:color=0x55ebc8@0.35:t=3:enable='between(n,%d,%d)'"%(x-8,y-8,w+16,h+16,start+3,end-3))
    return ",".join(out)
