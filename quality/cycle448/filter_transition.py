"""Cycle448: genre-neutral 8-to-2 animated filtering. REVIEW ONLY, self-drawn."""
from __future__ import annotations
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
W,H,FPS,N=1080,1920,30,75
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def validate(story):
    if story.get('asset_rights')!='SELF_DRAWN_SYNTHETIC':raise ValueError('rights')
    if story.get('publication_status')!='NOT_APPROVED' or story.get('auto_post',False):raise ValueError('publication')
    rows=story.get('rows',[])
    if len(rows)!=8 or len({r.get('id') for r in rows})!=8:raise ValueError('unique rows')
    if any(r.get('status') not in ('対応済','未対応') for r in rows):raise ValueError('status')
    opened=[r for r in rows if r['status']=='未対応']
    if not opened or len(opened)!=story.get('open_count'):raise ValueError('source/result mismatch')
    return rows,opened

def ease(x):
    x=max(0.,min(1.,float(x)))
    return x*x*(3-2*x)

def state_at(frame,rows):
    if not 0<=frame<N:raise ValueError('frame out of range')
    collapse=ease((frame-34)/21);fade=1-ease((frame-17)/18)
    result=[];opened_index=0
    for i,r in enumerate(rows):
        pending=r['status']=='未対応'
        if pending:
            y=638+(i*(1-collapse)+opened_index*collapse)*108
            opened_index+=1
        else:y=638+i*108
        result.append({'id':r['id'],'status':r['status'],'y':round(y,3),'alpha':round(1. if pending else fade,5)})
    return result

def f(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def background():
    im=Image.new('RGB',(W,H),'#071321');d=ImageDraw.Draw(im)
    d.rounded_rectangle((42,40,1038,130),radius=24,fill='#12364d')
    d.text((74,66),'AI時短ラボ  /  架空データの実演',font=f(30,True),fill='#3de5e6')
    d.text((978,82),'05/08',font=f(26),anchor='rm',fill='#b2c9d8')
    d.line((72,162,1008,162),fill='#22536a',width=3)
    d.text((72,212),'未対応だけを残す',font=f(65,True),fill='#f3f8ff')
    d.text((74,313),'8件 → 2件  フィルターの動きを確認',font=f(35),fill='#a8c6d7')
    d.rounded_rectangle((72,502,1008,605),radius=20,fill='#175375')
    for x,s in [(110,'受注ID'),(510,'対応状況'),(847,'確認')]:
        d.text((x,527),s,font=f(36,True),fill='#f3f8ff')
    d.rounded_rectangle((70,1680,1010,1785),radius=22,fill='#122e43')
    d.text((100,1710),'FILTER / 架空の対応記録を抽出',font=f(34,True),fill='#f3f8ff')
    d.text((72,1855),'DEMO / 架空の受注ID  •  REVIEW ONLY',font=f(25),fill='#7e9cac')
    return im

def frame(story,n,bg=None):
    rows,opened=validate(story)
    im=(bg or background()).copy()
    for r in state_at(n,rows):
        a=r['alpha']
        if a<=.003:continue
        y=int(r['y']);pending=r['status']=='未対応'
        lay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(lay)
        d.rounded_rectangle((72,y,1008,y+92),radius=16,
            fill=(62,42,66,int(250*a)) if pending else (28,65,83,int(235*a)),
            outline=(255,109,135,int(255*a)) if pending else None,width=4)
        for x,s,c in [(110,r['id'],(243,248,255)),(550,r['status'],(255,109,135) if pending else (138,240,208)),
                      (880,'●' if pending else '✓',(255,109,135) if pending else (138,240,208))]:
            d.text((x,y+24),s,font=f(35,True),fill=(*c,int(255*a)))
        im=Image.alpha_composite(im.convert('RGBA'),lay).convert('RGB')
    if n>=40:
        a=ease((n-40)/18)
        lay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(lay)
        d.rounded_rectangle((110,1015,970,1250),radius=28,fill=(20,82,102,int(235*a)),
                            outline=(61,229,230,int(255*a)),width=4)
        d.text((540,1070),'抽出結果：未対応 2件',font=f(53,True),anchor='mt',fill=(243,248,255,int(255*a)))
        d.text((540,1160),'8件中2件を確認',font=f(37),anchor='mt',fill=(255,206,104,int(255*a)))
        im=Image.alpha_composite(im.convert('RGBA'),lay).convert('RGB')
    return im

def render(story,out):
    validate(story);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    bg=background()
    for n in range(N):frame(story,n,bg).save(out/f'frame_{n:03d}.png',compress_level=1)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--story',required=True);p.add_argument('--output',required=True)
    a=p.parse_args()
    render(json.loads(Path(a.story).read_text(encoding='utf-8')),a.output)
