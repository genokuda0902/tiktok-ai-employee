"""Ten-genre animated chapter rail for 1080x1920 image-slide videos."""
import math
from PIL import Image, ImageDraw
WIDTH, HEIGHT, FPS, FRAME_COUNT, SCENE_COUNT = 1080, 1920, 30, 468, 8
RAIL_W, RAIL_H, RAIL_X, RAIL_Y = 792, 36, 64, 166
PALETTES = {
    'ai_work':'#40DFD2', 'beauty':'#FC99C3',
    'love_psychology':'#FFADD1', 'saving':'#8DEBAD',
    'sales_business':'#6ACDF5', 'career':'#A6BBFF',
    'health':'#81E2C1', 'science':'#4DEBDB',
    'travel_food':'#FFC275', 'product_comparison':'#C4AFFF'
}
def frame_scene(index):
    if not 0 <= index < FRAME_COUNT:
        raise ValueError('invalid frame')
    pos = index * SCENE_COUNT / FRAME_COUNT
    return min(int(pos),SCENE_COUNT-1),pos-int(pos)
def make_overlay(index,genre='science'):
    if genre not in PALETTES:
        raise ValueError('unknown genre')
    scene,phase=frame_scene(index)
    accent=tuple(bytes.fromhex(PALETTES[genre][1:]))
    im=Image.new('RGBA',(RAIL_W*2,RAIL_H*2),(0,0,0,0))
    d=ImageDraw.Draw(im,'RGBA')
    for j in range(SCENE_COUNT):
        x=j*198
        d.rounded_rectangle((x,24,x+174,46),radius=11,fill=(49,81,96,215))
        if j<scene:
            d.rounded_rectangle((x,24,x+174,46),radius=11,fill=(*accent,210))
        elif j==scene:
            eased=phase*phase*(3-2*phase)
            end=x+max(12,int(174*eased))
            d.rounded_rectangle((x,24,end,46),radius=11,fill=(*accent,255))
            glow=int(26*(.55+.45*math.sin(index*.18)**2))
            cx=min(end,x+169)
            d.ellipse((cx-16,16,cx+16,54),fill=(*accent,glow))
    return im.resize((RAIL_W,RAIL_H),Image.Resampling.LANCZOS)
