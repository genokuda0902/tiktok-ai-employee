"""Zero-cost, original Japanese infographic kinetic-focus component.
For human review only. No posting or paid services.
The full 22.5s local renderer and MP4 are in the separate review ZIP.
"""
import math
from PIL import ImageDraw

GENRES=("ai_work","business","money","learning","health","lifestyle","psychology","science","history","travel")
PALETTES={
"ai_work":"#58E5D8","business":"#71B8FF","money":"#F6CA76",
"learning":"#A4A1FF","health":"#6FE5B4","lifestyle":"#F5A5BF",
"psychology":"#CE9CF6","science":"#8FDDFB","history":"#E4BA8C",
"travel":"#81D8D3"}
# Illustration-only coordinates; all boxes exclude subtitle panel and TikTok UI zones.
FOCUS_BOXES=(
 ((82,631,998,784),(82,809,998,962),(82,987,998,1140)),
 ((82,631,998,784),(82,809,998,962),(82,987,998,1140)),
 ((82,631,490,1154),(590,631,998,1154)),
 ((82,631,998,784),(82,809,998,962),(82,987,998,1140)),
 ((82,631,998,784),(82,809,998,962),(82,987,998,1140)),
 ((82,636,998,848),(82,951,998,1164)),
 ((166,650,914,1169),),
 ((82,631,998,784),(82,809,998,962),(82,987,998,1140)),
)
def rgb(h):
 return tuple(int(h[i:i+2],16) for i in (1,3,5))
def mix(a,b,f):
 return tuple(round(a[i]*(1-f)+b[i]*f) for i in range(3))
def focus_index(scene,elapsed,duration):
 if not (0<=scene<8) or duration<=0:raise ValueError("Invalid scene/duration")
 n=len(FOCUS_BOXES[scene])
 return min(n-1,int(max(0,min(.999999,elapsed/duration))*n))
def draw_focus(image,scene,elapsed,duration,genre="ai_work"):
 """Draw a subtle breathing focus outline and moving accent on a PIL RGB slide."""
 if genre not in GENRES:raise ValueError("Unknown genre")
 box=FOCUS_BOXES[scene][focus_index(scene,elapsed,duration)]
 accent=rgb(PALETTES[genre]);d=ImageDraw.Draw(image)
 pulse=.5+.5*math.sin(2*math.pi*elapsed*1.15)
 border=mix(accent,(29,65,80),.24+.22*(1-pulse))
 x1,y1,x2,y2=box
 d.rounded_rectangle(box,radius=30,outline=border,width=5)
 d.rounded_rectangle((x1+6,y1+6,x2-6,y2-6),radius=25,
                     outline=mix(border,(20,47,63),.62),width=2)
 x=int(x1+52+(x2-x1-104)*((elapsed*.43)%1))
 d.rounded_rectangle((x-34,y1-4,x+34,y1+4),radius=4,fill=accent)
 return image
