"""Offline speech-energy meter; no transcription, identification or posting."""
from PIL import Image, ImageDraw
import math
SIZE=(160,112)
PALETTES={
 'ai_work':'#58E5D8','business':'#71B8FF','money':'#F6CA76',
 'learning':'#A4A1FF','health':'#6FE5B4','lifestyle':'#F5A5BF',
 'psychology':'#CE9CF6','science':'#8FDDFB','history':'#E4BA8C',
 'travel':'#81D8D3'
}
def energy_level(rms,noise_floor=0.0014,reference=0.050):
 if not math.isfinite(rms) or rms<0: raise ValueError('rms must be nonnegative finite')
 if not (0<noise_floor<reference): raise ValueError('invalid floor/reference')
 if rms<=noise_floor:return 0.
 return min(1.,max(0.,math.log(rms/noise_floor)/math.log(reference/noise_floor)))
def meter_frame(level,genre='ai_work',frame=0):
 if genre not in PALETTES:raise ValueError('unsupported genre')
 if not math.isfinite(level) or not (0<=level<=1):raise ValueError('level outside 0..1')
 accent=tuple(bytes.fromhex(PALETTES[genre][1:]))
 im=Image.new('RGBA',SIZE,(0,0,0,0));d=ImageDraw.Draw(im)
 d.rounded_rectangle((5,8,155,104),radius=22,fill=(14,43,60,226),outline=(*accent,90),width=2)
 for i in range(7):
  sway=0.64+0.36*math.sin(frame*.17+i*.82)**2
  h=7+int(67*level*sway);x=22+18*i;y=55-h//2
  d.rounded_rectangle((x,y,x+10,y+h),radius=5,fill=(*accent,100 if level<.08 else 232))
 return im
