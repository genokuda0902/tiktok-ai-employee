"""Cycle543 text-safe cinematic lighting maps for ten genre templates."""
from pathlib import Path
import numpy as np
from PIL import Image

W,H=1080,1920
GENRES={
"AI・仕事効率化":(110,211,242),"美容・身だしなみ":(250,192,184),
"恋愛・心理":(247,162,203),"お金・節約":(231,204,119),
"営業・ビジネス":(162,204,252),"転職・キャリア":(193,195,255),
"健康・生活改善":(151,226,186),"雑学・科学":(150,228,239),
"旅行・グルメ":(252,201,139),"商品比較・暮らし":(204,220,236)}
TIMES=[0,1.77,3.52,5.50,6.55,7.66,9.48,11.18,12.5]

def gaussian(x,y,cx,cy,sx,sy):
    return np.exp(-.5*((x-cx)/sx)**2-.5*((y-cy)/sy)**2)

def make_light_map(scene:int,color:tuple[int,int,int],output:Path):
    """A procedural key, rim and bounce light, absent outside 565..1360px."""
    assert 0<=scene<8
    output.parent.mkdir(parents=True,exist_ok=True)
    yy,xx=np.ogrid[:H,:W]
    sign=1 if scene%2==0 else -1
    key=gaussian(xx,yy,540+sign*190,850,240,280)
    rim=gaussian(xx,yy,540-sign*360,1030,160,350)
    bounce=gaussian(xx,yy,540,1260,380,100)
    gate=np.clip((yy-565)/105,0,1)*np.clip((1360-yy)/125,0,1)
    alpha=np.clip((.33*key+.20*rim+.050*bounce)*gate,0,.39)
    base=np.array(color,dtype=np.float32)
    if scene%3==0:base=.80*base+.20*np.array([255,221,172])
    elif scene%3==1:base=.78*base+.22*np.array([177,228,255])
    rgba=np.empty((H,W,4),dtype=np.uint8)
    rgba[:,:,:3]=np.broadcast_to(base.astype(np.uint8),(H,W,3))
    rgba[:,:,3]=np.round(alpha*255).astype(np.uint8)
    Image.fromarray(rgba,"RGBA").save(output,optimize=True)
    return {"scene":scene,"max_alpha":float(alpha.max()),
            "max_top_alpha":int(rgba[:565,:,3].max()),
            "max_bottom_alpha":int(rgba[1360:,:,3].max())}
