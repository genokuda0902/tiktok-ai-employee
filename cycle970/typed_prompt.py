#!/usr/bin/env python3
"""Review-only animated Japanese prompt demonstration; NOT a real ChatGPT recording.

Uses a local review MP4. Never uploads source or enables publication.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,CAPTION_TOP=1080,1920,30,1490
START,END=261,348
LINES=('この売上データを月別に集計して','4〜6月の営業AとBを比較し','表とグラフで要点をまとめて')
GENRES={'ai_work':'#00D5D4','business':'#60A5FA','finance':'#FBBF24','health':'#34D399','beauty':'#FB7185','travel':'#38BDF8','education':'#A78BFA','food':'#FB923C','life_hacks':'#2DD4BF','tech':'#818CF8'}
REVIEWED=frozenset({'ai_work'})

def check_genre(g):
    if g not in GENRES: raise ValueError('Unknown genre')
    if g not in REVIEWED: raise PermissionError('Unreviewed genre; fail closed')

def font(sz,bold=False):
    name='NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'
    for folder in ('/usr/share/fonts/opentype/noto','/usr/share/fonts/truetype/noto'):
        p=Path(folder)/name
        if p.exists(): return ImageFont.truetype(str(p),sz,index=0)
    raise RuntimeError('Japanese Noto font missing; fail closed')

def visible_text(phase):
    """Return incremental typing of all three lines, completed before Send."""
    total=sum(map(len,LINES)); n=min(total,max(0,int(phase/0.82*total)))
    out=[]
    for s in LINES:
        out.append(s[:max(0,min(len(s),n))]); n-=len(s)
    return out

def scene(phase,g='ai_work'):
    check_genre(g); accent=GENRES[g]
    im=Image.new('RGB',(W,CAPTION_TOP),'#071725'); d=ImageDraw.Draw(im)
    d.rounded_rectangle((35,36,1045,1435),radius=32,fill='#0C2335',outline='#2C5467',width=3)
    d.rounded_rectangle((64,67,1016,149),radius=18,fill='#12334B')
    d.ellipse((90,94,117,121),fill=accent)
    d.text((139,84),'AI ASSISTANT  /  操作イメージ',font=font(34,True),fill='#D7F7FF')
    d.text((64,202),'AIへの指示を',font=font(71,True),fill='white')
    d.text((64,305),'実際に組み立てる',font=font(65,True),fill='white')
    d.text((66,416),'目的・条件・出力を1つの文章に',font=font(38),fill='#B7D5E4')
    d.rounded_rectangle((62,516,1018,1136),radius=28,fill='#F1F7FC')
    d.text((103,560),'指示内容',font=font(42,True),fill='#173950')
    d.line((102,641,973,641),fill='#B9CBD6',width=3)
    typed=visible_text(phase)
    for i,s in enumerate(typed):
        if s: d.text((104,695+i*113),s,font=font(44,True),fill='#173950')
    active=max((i for i,s in enumerate(typed) if s),default=0)
    if phase<0.84 and int(phase*FPS*2)%2==0:
        x=104+int(d.textlength(typed[active],font=font(44,True)))
        d.rounded_rectangle((x+3,703+active*113,x+8,754+active*113),radius=2,fill='#087CBA')
    d.rounded_rectangle((65,1178,1015,1302),radius=22,fill='#16435B')
    d.text((94,1211),'内容を確認してから送信',font=font(42,True),fill='#D7EDF8')
    d.rounded_rectangle((791,1196,989,1282),radius=18,fill=accent if phase>=0.84 else '#477183')
    d.text((830,1211),'送信',font=font(43,True),fill='#042638' if phase>=0.84 else '#DAE6EB')
    if phase>=0.84:
        d.line([(946,1278),(976,1313),(981,1294),(1000,1288),(946,1278)],fill='#FFFFFF',width=7)
    d.text((66,1354),'再現画面 / 実際のChatGPT操作録画ではありません',font=font(27),fill='#B7CEDA')
    return np.asarray(im)

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def audio_activity(p):
    """Energy-only voice activity diagnostic, NOT speech recognition."""
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','16000','-f','s16le','pipe:1'])
    a=np.frombuffer(raw,dtype='<i2').astype(np.float32)/32768
    chunk=320; n=len(a)//chunk
    if not n:return {'status':'NO_AUDIO'}
    rms=np.sqrt(np.mean(a[:n*chunk].reshape(n,chunk)**2,axis=1))
    return {'status':'ENERGY_ONLY','window_ms':20,'threshold_rms':0.012,'active_fraction':round(float(np.mean(rms>0.012)),4),'mean_rms':round(float(rms.mean()),5)}

def render(source,output,report,genre='ai_work',synthetic=False):
    check_genre(genre); source,output,report=map(Path,(source,output,report))
    if source.resolve()==output.resolve():raise ValueError('Source and output must differ')
    cap=cv2.VideoCapture(str(source)); nframes=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w,h=int(cap.get(3)),int(cap.get(4)); fps=cap.get(5)
    if (w,h)!=(W,H) or abs(fps-FPS)>.01:raise ValueError('Unexpected geometry')
    if not synthetic and nframes!=691:raise ValueError('Unexpected private source length')
    start,end=(30,min(90,nframes)) if synthetic else (START,END)
    if nframes<end:raise ValueError('Source too short')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(source),'-map','0:v','-map','1:a:0','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart','-frames:v',str(nframes),str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    count=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if start<=count<end:
                frame[:CAPTION_TOP]=cv2.cvtColor(scene((count-start)/(end-start),genre),cv2.COLOR_RGB2BGR)
            proc.stdin.write(frame.tobytes());count+=1
        proc.stdin.close();err=proc.stderr.read().decode('utf8','replace')
        if proc.wait():raise RuntimeError(err[-2000:])
    finally:
        cap.release()
        if proc.poll() is None:proc.kill()
    if count!=nframes:raise RuntimeError('Frame count mismatch')
    data={'input_sha256':sha(source),'output_sha256':sha(output),'frames':count,'fps':FPS,'resolution':[W,H],'changed_frames':[start,end],'genre':genre,'audio_energy':audio_activity(output),'independent_japanese_asr':'UNVERIFIED','subtitle_semantic_timing':'UNVERIFIED','publication_approved':False,'employee_approval':False,'source_rights':'UNVERIFIED','synthetic_ci_only':bool(synthetic)}
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');p.add_argument('--synthetic',action='store_true')
    a=p.parse_args();print(json.dumps(render(a.source,a.output,a.report,a.genre,a.synthetic),ensure_ascii=False))
