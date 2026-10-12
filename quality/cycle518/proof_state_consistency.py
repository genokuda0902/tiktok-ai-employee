#!/usr/bin/env python3
"""Cycle518: cross-scene monotonic evidence state (no verified -> pending regressions).
Synthetic data, review-only; a new reimplementation, NOT recovered v33.
No external assets, posting, or network calls.
"""
import argparse
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=540,625,30
START,END=15.,17.5
GENRES=frozenset(('ai_work','beauty','relationship','money','sales','career','health','science','travel','products'))
STATES=('input','calculating','verified')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def validate(m):
    if m.get('genre') not in GENRES: raise ValueError('genre')
    if m.get('rights')!='synthetic_local_review_only' or m.get('privacy_checked') is not True: raise ValueError('rights')
    if (m.get('human_review'),m.get('publication'),m.get('auto_post'))!=('HUMAN_REVIEW','NOT_APPROVED',False): raise ValueError('publication gate')
    v=m.get('values'); labels=m.get('labels')
    if not isinstance(v,list) or len(v)!=4 or any(type(x)!=int or not 0<=x<=9999 for x in v): raise ValueError('values')
    if not isinstance(labels,list) or len(labels)!=4 or any(type(x)!=str or not 1<=len(x)<=6 for x in labels): raise ValueError('labels')
    if sum(v)>99999: raise ValueError('sum')
    if type(m.get('claimed_total')) is not int or m['claimed_total'] != sum(v):
        raise ValueError('unverified or mismatched total')
    events=m.get('proof_events')
    if not isinstance(events,list) or len(events)<3: raise ValueError('missing proof events')
    previous_t=-1.0; previous_state=-1
    for ev in events:
        if not isinstance(ev,dict) or type(ev.get('at')) not in (int,float) or ev.get('state') not in STATES:
            raise ValueError('bad proof event')
        t=float(ev['at']); rank=STATES.index(ev['state'])
        if t<=previous_t or rank<previous_state: raise ValueError('proof state went backwards')
        previous_t,previous_state=t,rank
    if previous_state != 2 or next((e['at'] for e in events if e['state']=='verified'),float('inf'))>=START:
        raise ValueError('verified state must predate proof scene')
    if any(e['state']=='calculating' for e in events if e['at']>=START):
        raise ValueError('cannot revert to calculating after verification')
    return m

def final_total(m,t):
    """Result was verified in an earlier scene, so it must persist from first frame."""
    validate(m)
    if not 0 <= t <= END-START: raise ValueError('scene-relative time out of range')
    return m['claimed_total']

def state_at(m,absolute_time):
    """Monotonic state lookup shared by any of ten genres."""
    validate(m)
    state='input'
    for event in m['proof_events']:
        if absolute_time >= event['at']: state=event['state']
        else: break
    return state

def ease(t):
    t=max(0.,min(1.,t));return t*t*(3-2*t)

def font(n,bold=False): return ImageFont.truetype(BOLD if bold else FONT,n)

def card(d,box,fill,stroke='#367588',radius=14):
    d.rounded_rectangle(box,radius=radius,fill=fill,outline=stroke,width=2)

def frame(m,t):
    validate(m)
    im=Image.new('RGB',(W,H),'#081d30');d=ImageDraw.Draw(im)
    for y in range(H):
        f=y/H;d.line((0,y,W,y),fill=(int(7+8*f),int(25+12*f),int(42+13*f)))
    card(d,(14,12,526,70),'#10334a')
    d.text((28,24),'AI時短ラボ',font=font(22,True),fill='#8ae8e5')
    d.text((337,34),'架空データ / 再現',font=font(14),fill='#d5e5ec')
    d.text((22,86),'同じ数字で、結果を検証',font=font(28,True),fill='white')
    d.text((24,132),'12.5秒で検算完了 → 結果を保持',font=font(18),fill='#a9d5e2')
    card(d,(15,184,258,550),'#253043','#d57e98')
    card(d,(282,184,525,550),'#17444a','#67dec6')
    card(d,(25,195,248,239),'#b85b7a','#b85b7a',10)
    card(d,(292,195,515,239),'#1ca98d','#1ca98d',10)
    d.text((42,204),'BEFORE',font=font(23,True),fill='white')
    d.text((310,204),'AFTER',font=font(23,True),fill='white')
    d.text((30,254),'表を見て手計算',font=font(18,True),fill='#ffd3e0')
    for i,(lab,val) in enumerate(zip(m['labels'],m['values'])):
        y=291+42*i
        card(d,(30,y,243,y+35),'#324d60','#324d60',6)
        d.text((41,y+5),lab,font=font(16),fill='#f0f4fa')
        d.text((171,y+4),str(val),font=font(19,True),fill='white')
    card(d,(30,475,243,531),'#483142','#483142',10)
    d.text((42,487),'＋ 手で合計…',font=font(18,True),fill='#ffbcd0')
    d.text((294,254),'検算済みの結果',font=font(18,True),fill='#a2ffe2')
    d.line((304,439,507,439),fill='#a9c8cf',width=2)
    peak=max(1,max(m['values']))
    for i,(lab,val) in enumerate(zip(m['labels'],m['values'])):
        x=312+i*48; p=ease((t-.25-i*.14)/1.05)
        bh=max(1,int(116*val/peak*p))
        d.rounded_rectangle((x,439-bh,x+29,439),radius=4,fill='#36aee1' if i<3 else '#68e0c2')
        d.text((x,445),lab,font=font(12),fill='#d4e5eb')
    card(d,(292,473,516,533),'#206259','#3ed5b5',10)
    total=final_total(m,t)
    d.text((301,487),'合計',font=font(17,True),fill='#b5ffdf')
    d.text((388,481),str(total),font=font(29,True),fill='white')
    d.rounded_rectangle((296,280,514,313),radius=8,fill='#1d765f')
    d.text((302,283),'検算済み / B6',font=font(17,True),fill='#eafff3')
    arrow_x=258+int(4*math.sin(5*t))
    d.polygon([(arrow_x,353),(arrow_x+15,353),(arrow_x+15,346),(arrow_x+29,369),(arrow_x+15,392),(arrow_x+15,385),(arrow_x,385)],fill='#f5d873')
    d.text((20,578),'※ 数字は架空。実際の業務改善実績ではありません。',font=font(13),fill='#c1d9e4')
    d.rounded_rectangle((24,604,516,610),radius=3,fill='#28485b')
    d.rounded_rectangle((24,604,24+int(492*min(1,t/2.5)),610),radius=3,fill='#62d7bd')
    return im

def run(cmd): subprocess.run(cmd,check=True)

def render(manifest,base,out,work):
    m=validate(json.loads(Path(manifest).read_text(encoding='utf-8')))
    base,out,work=Path(base),Path(out),Path(work)
    if not base.is_file(): raise FileNotFoundError(base)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(base)]))
    vs=[s for s in probe['streams'] if s['codec_type']=='video']
    if not vs or (vs[0]['width'],vs[0]['height'])!=(1080,1920): raise ValueError('1080x1920 required')
    if not any(s['codec_type']=='audio' for s in probe['streams']): raise ValueError('audio missing')
    if abs(float(probe['format']['duration'])-20)>.05: raise ValueError('20 seconds required')
    frames=work/'frames';frames.mkdir(parents=True,exist_ok=True)
    for i in range(round((END-START)*FPS)): frame(m,i/FPS).save(frames/f'{i:03d}.png')
    overlay=work/'proof.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(FPS),'-i',str(frames/'%03d.png'),'-vf','scale=1080:1250:flags=lanczos,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','20',str(overlay)])
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(base),'-i',str(overlay),'-filter_complex',f"[1:v]setpts=PTS-STARTPTS+{START}/TB[proof];[0:v][proof]overlay=0:0:eof_action=pass:enable='gte(t,{START})*lt(t,{END})',format=yuv420p[v]",'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-r','30','-c:a','copy','-movflags','+faststart',str(out)])
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--base',required=True);p.add_argument('--out',required=True);p.add_argument('--work',required=True)
    a=p.parse_args();render(a.manifest,a.base,a.out,a.work)
