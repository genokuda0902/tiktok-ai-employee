"""Cycle2063: reusable five-scene progress indicator (Pillow)."""
from PIL import Image, ImageDraw

def make_markers(size=(1080,1920), count=5):
    """Return transparent RGBA overlays, one per active chapter."""
    overlays=[]
    for active in range(count):
        im=Image.new("RGBA",size,(0,0,0,0))
        d=ImageDraw.Draw(im)
        for i in range(count):
            y=520+i*55
            r=9 if i==active else 5
            color=(245,196,94,235) if i==active else (245,245,245,105)
            d.ellipse((35-r,y-r,35+r,y+r),fill=color)
        overlays.append(im)
    return overlays

def scene_at(t,duration,count=5):
    if duration<=0 or count<=0: raise ValueError("invalid duration/count")
    return min(count-1,max(0,int(t/duration*count)))
