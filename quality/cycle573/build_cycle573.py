"""Cycle573 preview-only renderer. Exact MP4 builder is in user ZIP."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).parent
CFG=json.loads((ROOT/'config/genres.json').read_text())
W,H,N=980,1060,66
def smooth(t):
 t=max(0,min(1,t))
 return t*t*(3-2*t)
def draw_frame(n,genre='雑学・科学'):
 if not 0<=n<N:raise ValueError('frame index')
 if genre not in CFG['genres']:raise ValueError('genre')
 color=CFG['genres'][genre]['theme']
 im=Image.new('RGB',(980,980),'#081c2a')
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((60,140,920,770),radius=35,outline=color,width=8)
 d.rounded_rectangle((360,330,620,600),radius=25,fill='#102d3c',outline=color,width=5)
 for j in range(10):
  y=190+j*52
  if smooth((n-j*2)/30)>.4:d.line((90,y,340,y),fill=color,width=4)
 stage=0 if n<18 else 1 if n<42 else 2
 d.rectangle((80+stage*280,860,300+stage*280,880),fill=color)
 return im
