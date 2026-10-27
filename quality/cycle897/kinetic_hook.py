"""Offline kinetic hook and 8-scene progress renderer; review-only, no publishing."""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
SIZE=(1080,1920)
CARD_SIZE=(940,1000)
CARD_ORIGIN=(70,357)
RAIL_ORIGIN=(72,1738)
SCENE_BOUNDS=(0,2.9,5.8,8.95,11.35,14.3,17,19.6,691/30)
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
NAVY=(14,32,60); GREY=(89,108,136)

@dataclass(frozen=True)
class HookCopy:
    question:str='まず、何から始める？'
    answer:str='繰り返す作業を1つ選ぶ'
    example:str='例：週次報告をまとめる'
    def validate(self):
        for s,limit in ((self.question,16),(self.answer,18),(self.example,22)):
            if not s or len(s)>limit or any(x in s for x in ('@','http','％改善','%改善','絶対','保証')):
                raise ValueError('Unsafe or unfit copy')

def font(size,bold=False):
    return ImageFont.truetype(BOLD if bold else FONT,size,index=0)

def text_fit(draw,xy,s,width,initial=62,bold=True,fill=NAVY):
    for z in range(initial,29,-1):
        f=font(z,bold)
        if draw.textbbox((0,0),s,font=f)[2]<=width:
            draw.text(xy,s,font=f,fill=fill)
            return z
    raise ValueError('Text too long')

def rounded(draw,rect,fill,radius=22,outline=None,width=2):
    draw.rounded_rectangle(rect,radius=radius,fill=fill,outline=outline,width=width)

def stage_panel(stage:int,copy:HookCopy)->Image.Image:
    copy.validate()
    if stage not in (0,1,2):raise ValueError('stage')
    im=Image.new('RGBA',CARD_SIZE,(0,0,0,0));d=ImageDraw.Draw(im)
    rounded(d,(0,0,939,998),(243,248,255,255),36)
    rounded(d,(40,40,900,116),(218,238,253,255),22)
    d.text((65,52),'AI WORKFLOW  /  START',font=font(37,True),fill=(20,90,156,255))
    d.text((735,57),f'0{stage+1} / 03',font=font(30,True),fill=(20,90,156,255))
    if stage==0:
        text_fit(d,(65,176),copy.question,815,65)
        d.text((68,271),'AI活用は、手順を決めるところから。',font=font(37),fill=GREY)
        rounded(d,(66,370,874,790),(229,241,253,255),30)
        for i,(title,sub) in enumerate((('作業','繰り返す仕事'),('見本','完成形の例'),('指示','目的と条件'))):
            y=414+i*115
            rounded(d,(98,y,842,y+91),(255,255,255,255),19)
            rounded(d,(117,y+15,177,y+75),(30,193,172,255) if i==0 else (25,118,221,255),17)
            d.text((134,y+19),str(i+1),font=font(37,True),fill='white')
            d.text((210,y+14),title,font=font(40,True),fill=NAVY)
            d.text((450,y+21),sub,font=font(29),fill=GREY)
        rounded(d,(72,843,868,930),(16,54,98,255),19)
        d.text((148,857),'まずは「作業を整理」から',font=font(42,True),fill='white')
    elif stage==1:
        text_fit(d,(65,170),'作業 → 見本 → 指示',820,66)
        d.text((68,265),'順番が見えると、次の行動が決まる。',font=font(36),fill=GREY)
        for i,(title,sub) in enumerate((('01  作業','何を繰り返している？'),('02  見本','完成形はどんな形？'),('03  指示','目的と条件を明確に'))):
            y=360+i*175
            rounded(d,(68,y,870,y+142),(222,247,243,255) if i==0 else (255,255,255,255),24,(31,193,169,255) if i==0 else (198,215,233,255),4)
            d.text((105,y+12),title,font=font(44,True),fill=(12,91,131,255))
            d.text((106,y+75),sub,font=font(34),fill=NAVY)
        rounded(d,(68,907,870,961),(212,231,248,255),17)
        d.text((280,914),'この順番で進める',font=font(31,True),fill=(22,100,173,255))
    else:
        text_fit(d,(65,171),'最初にやること',820,69)
        d.text((68,271),'今日の仕事から、1つだけ選ぶ。',font=font(37),fill=GREY)
        rounded(d,(68,368,870,785),(222,247,243,255),32,(35,190,170,255),5)
        rounded(d,(105,409,210,514),(29,192,169,255),28)
        d.text((134,424),'✓',font=font(66,True),fill='white')
        text_fit(d,(113,555),copy.answer,730,56)
        rounded(d,(110,659,826,743),(255,255,255,255),20)
        text_fit(d,(132,676),copy.example,664,39,bold=False)
        rounded(d,(68,854,870,946),(18,57,99,255),22)
        d.text((224,872),'次の場面で具体例へ',font=font(42,True),fill='white')
    return im

def smooth(x):
    x=max(0.,min(1.,x))
    return x*x*(3-2*x)

def hook_frame(n:int,copy:HookCopy,panels=None)->Image.Image:
    if not 0<=n<87:raise ValueError('hook frame')
    panels=panels or [stage_panel(i,copy) for i in range(3)]
    t=n/FPS
    if t<.92:return panels[0]
    if t<1.08:return Image.blend(panels[0],panels[1],smooth((t-.92)/.16))
    if t<1.84:return panels[1]
    if t<2.0:return Image.blend(panels[1],panels[2],smooth((t-1.84)/.16))
    return panels[2]

def scene_index(t):
    for i in range(8):
        if SCENE_BOUNDS[i]<=t<SCENE_BOUNDS[i+1]:return i
    return 7

def rail_frame(n:int)->Image.Image:
    if not 0<=n<691:raise ValueError('rail frame')
    t=n/FPS;i=scene_index(t)
    start,end=SCENE_BOUNDS[i:i+2]
    fraction=smooth((t-start)/(end-start))
    im=Image.new('RGBA',(945,18),(0,0,0,0));d=ImageDraw.Draw(im)
    x=120*i
    rounded(d,(x,1,x+102,15),(68,92,121,255),7)
    if fraction>.02:
        length=max(7,round(102*fraction))
        rounded(d,(x,1,x+length,15),(42,219,201,255),7)
    return im

def render(out:Path,copy:HookCopy=HookCopy()):
    copy.validate()
    (out/'hook').mkdir(parents=True,exist_ok=True)
    (out/'rail').mkdir(parents=True,exist_ok=True)
    panels=[stage_panel(i,copy) for i in range(3)]
    for n in range(87):hook_frame(n,copy,panels).save(out/'hook'/f'{n:04d}.png',optimize=True)
    for n in range(691):rail_frame(n).save(out/'rail'/f'{n:04d}.png',optimize=True)
    return {'hook_frames':87,'rail_frames':691,'size':SIZE,'genres_supported':len(GENRES)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    print(render(p.parse_args().output))
