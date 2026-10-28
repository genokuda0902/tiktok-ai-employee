"""Original UI cursor overlays for TikTok slides. Human review only."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

FPS = 30
SIZE = (1080, 1920)
SCENE_START = 8.7
SCENE_DURATION = 2.9
STEPS = ((0.35, 0.98, 642, 0.74), (0.98, 1.90, 762, 1.53), (1.90, 2.88, 884, 2.44))
GENRE_COLORS = {
    "ai_productivity": "#24E0CF", "business": "#F2B94B",
    "finance": "#42CDA0", "education": "#66A7FF",
    "health": "#80D3AC", "beauty": "#EF9CC7",
    "food": "#F5A35D", "travel": "#6CC7E5",
    "lifestyle": "#C2A4F3", "technology": "#44D8E3",
}

def smoothstep(x):
    v = max(0., min(1., x))
    return v*v*(3-2*v)

def cursor_state(t):
    if t < 0.35 or t >= SCENE_DURATION:
        return None
    for idx,(start,end,y,click) in enumerate(STEPS):
        if start <= t < end:
            from_y = STEPS[idx-1][2] if idx else y-35
            yy = from_y + (y-from_y)*smoothstep((t-start)/0.22)
            xx = 820-112*smoothstep((t-start)/0.24) if idx == 0 else 708
            pulse = max(0.,1.-abs(t-click)/0.24)
            return xx,yy,pulse
    return None

def render_frame(t,genre="ai_productivity"):
    if genre not in GENRE_COLORS:
        raise ValueError("Unknown genre: fail closed")
    canvas=Image.new("RGBA",SIZE,(0,0,0,0))
    state=cursor_state(t)
    if state is None:
        return canvas
    x,y,pulse=state
    d=ImageDraw.Draw(canvas,"RGBA")
    color=tuple(bytes.fromhex(GENRE_COLORS[genre][1:]))
    if pulse>0:
        radius=19+39*(1-pulse)
        d.ellipse((x-radius,y-radius,x+radius,y+radius),outline=(*color,int(170*pulse)),width=5)
        radius2=10+16*(1-pulse)
        d.ellipse((x-radius2,y-radius2,x+radius2,y+radius2),fill=(*color,int(65*pulse)))
    points=[(x,y),(x+4,y+43),(x+14,y+33),(x+26,y+58),(x+40,y+52),(x+27,y+29),(x+46,y+28)]
    d.polygon([(a+5,b+7) for a,b in points],fill=(0,8,22,130))
    d.polygon(points,fill=(248,252,255,245))
    d.line(points+[points[0]],fill=(3,24,43,255),width=5,joint="curve")
    return canvas

def render_sequence(output,genre="ai_productivity"):
    output=Path(output)
    output.mkdir(parents=True,exist_ok=True)
    n=round(SCENE_DURATION*FPS)
    for i in range(n):
        render_frame(i/FPS,genre).save(output/f"{i:03d}.png",optimize=True)
    return n

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--genre",choices=list(GENRE_COLORS),default="ai_productivity")
    args=p.parse_args()
    print(render_sequence(args.out,args.genre))
