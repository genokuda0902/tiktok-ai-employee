#!/usr/bin/env python3
"""cycle974: source-linked arithmetic verification scene, private review only.

A deliberately fictional unverified AI draft (45) is compared against actual
arithmetic of the fictional 4-6 month data from cycle972 (46). No claims about
real AI behavior or Excel recordings. Keeps original AAC and burned captions.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,ART_BOTTOM=1080,1920,30,1240
START,END=435,522
REVIEWED=frozenset({'ai_work'})
GENRES={'ai_work':'#36E4D0','business':'#60A5FA','finance':'#FBBF24','health':'#34D399','beauty':'#FB7185','travel':'#38BDF8','education':'#A78BFA','food':'#FB923C','life_hacks':'#2DD4BF','tech':'#818CF8'}
FONT_DIR=Path('/usr/share/fonts/opentype/noto')

def require_genre(genre):
    if genre not in GENRES: raise ValueError('Unknown genre')
    if genre not in REVIEWED: raise PermissionError('Unreviewed genre: fail closed')

def load_verified_source():
    """Load the exact cycle972 source module; fail closed if missing or altered."""
    p=Path(__file__).resolve().parents[1]/'cycle972'/'chart_reveal.py'
    if not p.is_file(): raise FileNotFoundError('cycle972 arithmetic source missing')
    spec=importlib.util.spec_from_file_location('cycle972_source',p)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data={k:tuple(v) for k,v in module.DATA.items()}
    if tuple(module.MONTHS)!=('4月','5月','6月') or set(data)!={'営業A','営業B'}:raise ValueError('Unexpected upstream source schema')
    if any(len(v)!=3 or not all(isinstance(x,int) and x>=0 for x in v) for v in data.values()):raise ValueError('Invalid upstream data')
    totals={k:sum(v) for k,v in data.items()}
    if totals!=dict(module.TOTALS):raise ValueError('Upstream arithmetic drift')
    return data,totals

def font(size,bold=False):
    p=FONT_DIR/('NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc')
    if not p.is_file():raise RuntimeError('Japanese font missing: fail closed')
    return ImageFont.truetype(str(p),size,index=0)

def text(d,xy,s,size,color='#F3FBFF',bold=False):
    d.text(xy,s,font=font(size,bold),fill=color)

def stage(progress):
    if progress<0.30:return 0
    if progress<0.64:return 1
    return 2

def artwork(progress,genre='ai_work'):
    require_genre(genre)
    data,totals=load_verified_source()
    a=data['営業A'];b=data['営業B'];verified=totals['営業A']
    draft=verified-1
    accent=GENRES[genre];step=stage(progress)
    im=Image.new('RGB',(W,ART_BOTTOM),'#071A2B');d=ImageDraw.Draw(im)
    d.rounded_rectangle((40,25,1040,1210),radius=32,fill='#092638',outline='#347387',width=3)
    d.rounded_rectangle((69,54,1011,141),radius=19,fill='#123D51')
    text(d,(93,73),'VERIFY  /  元データで確かめる',37,'#D4F9FF',True)
    text(d,(78,166),'AIの答えは、最後に検算',58,'#FFFFFF',True)
    text(d,(82,249),'営業A｜4〜6月の架空データ',35,'#A7CFDC')
    d.rounded_rectangle((72,323,1008,533),radius=26,fill='#2E293C',outline='#9D6B8A',width=3)
    text(d,(104,342),'① AIの仮の下書き（未検証）',34,'#F5D9E8',True)
    text(d,(125,411),str(draft),79,'#FFADBC',True)
    text(d,(322,436),'そのまま採用しない',36,'#F5D9E8')
    active=step>=1
    d.rounded_rectangle((72,558,1008,792),radius=26,fill='#103A4C' if active else '#102D40',outline=accent if active else '#365A6D',width=4 if active else 2)
    text(d,(103,579),'② 元データの合計を確認',34,'#D4F6F7',True)
    formula=f'{a[0]} + {a[1]} + {a[2]} = {verified}'
    text(d,(119,653),formula if active else '4月 + 5月 + 6月 = ?',62,'#FFFFFF' if active else '#B1C5D3',True)
    if active:
        text(d,(119,733),f'営業Bも確認：{b[0]} + {b[1]} + {b[2]} = {totals["営業B"]}',29,'#B9DBE7')
    d.rounded_rectangle((72,817,1008,1093),radius=28,fill='#12453F' if step==2 else '#112F3D',outline=accent if step==2 else '#315C65',width=4 if step==2 else 2)
    text(d,(104,839),'③ 修正してから使う',36,'#D5FFF6',True)
    if step==2:
        text(d,(116,906),f'{draft}  →  {verified}',88,'#FFFFFF',True)
        text(d,(624,933),'差分 +1',40,accent,True)
        text(d,(116,1023),'元データと一致したか、最後に確認',30,'#C3E9E6')
    else:
        text(d,(116,931),'元データの確認待ち',45,'#AFC6D1')
    text(d,(85,1146),'※すべて説明用の架空例。実際のAI出力・操作録画ではありません。',23,'#A8C9D4')
    return im

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def aac_hash(path):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    h=hashlib.sha256()
    while True:
        chunk=p.stdout.read(65536)
        if not chunk:break
        h.update(chunk)
    err=p.stderr.read().decode('utf8','replace')
    if p.wait():raise RuntimeError('AAC extraction failed: '+err[-1000:])
    return h.hexdigest()

def render(source,output,report,genre='ai_work',synthetic=False):
    import cv2,numpy as np
    require_genre(genre)
    data,totals=load_verified_source()
    source,output,report=map(Path,(source,output,report))
    if source.resolve()==output.resolve():raise ValueError('Source and output must differ')
    cap=cv2.VideoCapture(str(source))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));w=int(cap.get(3));h=int(cap.get(4));fps=cap.get(5)
    if (w,h)!=(W,H) or abs(fps-FPS)>.01:raise ValueError('Source must be 1080x1920 at 30fps')
    if not synthetic and count!=691:raise ValueError('Unexpected review source length')
    start,end=(30,min(90,count)) if synthetic else (START,END)
    if count<end:raise ValueError('Source too short')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(source),'-map','0:v','-map','1:a:0','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart','-frames:v',str(count),str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    written=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if start<=written<end:
                art=np.asarray(artwork((written-start)/(end-start),genre))
                frame[:ART_BOTTOM]=cv2.cvtColor(art,cv2.COLOR_RGB2BGR)
            proc.stdin.write(frame.tobytes());written+=1
        proc.stdin.close();err=proc.stderr.read().decode('utf8','replace')
        if proc.wait():raise RuntimeError('Encoding failed: '+err[-2000:])
    finally:
        cap.release()
        if proc.poll() is None:proc.kill()
    if written!=count:raise RuntimeError('Frame count mismatch')
    before_aac=aac_hash(source);after_aac=aac_hash(output)
    if before_aac!=after_aac:raise RuntimeError('AAC changed')
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(output)],text=True))
    vs=next(s for s in p['streams'] if s['codec_type']=='video');aud=next(s for s in p['streams'] if s['codec_type']=='audio')
    if (vs['width'],vs['height'],vs['codec_name'])!=(W,H,'h264') or aud['codec_name']!='aac':raise RuntimeError('Codec mismatch')
    result={'source_sha256':sha(source),'output_sha256':sha(output),'duration_s':float(p['format']['duration']),'resolution':[W,H],'fps':FPS,'frames':written,'changed_frames':[start,end],'verified_totals':totals,'fictional_unverified_draft':totals['営業A']-1,'source_months':data,'aac_hash':after_aac,'aac_identical':True,'caption_region_preserved_from_y':ART_BOTTOM,'independent_japanese_asr':'NOT_AVAILABLE','subtitle_semantic_timing':'UNVERIFIED','rights':'UNVERIFIED','employee_approval':False,'publication_approved':False,'synthetic_ci_only':bool(synthetic)}
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');p.add_argument('--synthetic',action='store_true');a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.report,a.genre,a.synthetic),ensure_ascii=False,indent=2))
