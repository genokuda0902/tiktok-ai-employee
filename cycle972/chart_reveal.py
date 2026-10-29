#!/usr/bin/env python3
"""cycle972: original, fictional, grouped-bar source-data reveal.
Review-only. Never publishes, uploads private media, or approves content.
All frame art above y=1240; original burned Japanese captions and AAC retained.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,ART_BOTTOM=1080,1920,30,1240
START,END=348,435  # 11.60–14.50 seconds, source-check scene 05
MONTHS=("4月","5月","6月")
DATA={"営業A":(12,16,18),"営業B":(8,9,12)}
TOTALS={k:sum(v) for k,v in DATA.items()}
GENRES={"ai_work":"#25DED1","business":"#60A5FA","finance":"#FBBF24","health":"#34D399","beauty":"#FB7185","travel":"#38BDF8","education":"#A78BFA","food":"#FB923C","life_hacks":"#2DD4BF","tech":"#818CF8"}
REVIEWED=frozenset({"ai_work"})
FONT_DIR=Path('/usr/share/fonts/opentype/noto')

def require_genre(genre):
    if genre not in GENRES: raise ValueError('Unknown genre')
    if genre not in REVIEWED: raise PermissionError('Unreviewed genre; fail closed')

def font(size,bold=False):
    name='NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'
    p=FONT_DIR/name
    if not p.is_file():raise RuntimeError('Japanese font not found; fail closed')
    return ImageFont.truetype(str(p),size,index=0)

def ease(t):
    t=max(0.,min(1.,float(t)))
    return t*t*(3-2*t)

def visible_height(progress,index):
    return ease((progress-(0.075+index*0.22))/0.20)

def draw_text(d,xy,s,size,color='#FFFFFF',bold=False):
    d.text(xy,s,font=font(size,bold),fill=color)

def artwork(progress,genre='ai_work'):
    """Render only non-caption pixels, with arithmetic derived from DATA."""
    require_genre(genre)
    accent=GENRES[genre]
    im=Image.new('RGB',(W,ART_BOTTOM),'#061929')
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((39,28,1041,1212),radius=34,fill='#0A2638',outline='#2D6A80',width=3)
    d.rounded_rectangle((67,58,1013,144),radius=18,fill='#124055')
    draw_text(d,(92,77),'SOURCE DATA  /  数字を目で確認',36,'#D6FAFF',True)
    draw_text(d,(74,174),'元データと比較する',64,'#FFFFFF',True)
    draw_text(d,(78,265),'4〜6月｜営業Aと営業Bの月別比較',34,'#A9D2DF')
    d.rounded_rectangle((68,332,1012,917),radius=28,fill='#102E43',outline='#36667B',width=2)
    draw_text(d,(95,349),'月ごとの違いをグラフで確認',34,'#E6F9FD',True)
    # Small legend with distinct shape + text, not color alone.
    d.rounded_rectangle((615,402,649,430),radius=5,fill=accent)
    draw_text(d,(661,394),'営業A',30,'#E8F7FF')
    d.rounded_rectangle((795,402,829,430),radius=5,fill='#8C9CFF')
    draw_text(d,(841,394),'営業B',30,'#E8F7FF')
    top,bottom=473,835
    for v in (0,5,10,15,20):
        y=bottom-int(v/20*(bottom-top))
        d.line((140,y,966,y),fill='#2E4F60',width=2)
        draw_text(d,(86,y-20),str(v),26,'#9FC2D2')
    for i,month in enumerate(MONTHS):
        x=280+i*280
        phase=visible_height(progress,i)
        for j,(name,color) in enumerate((("営業A",accent),("営業B",'#8C9CFF'))):
            v=DATA[name][i]
            h=int(v/20*(bottom-top)*phase)
            bx=x-77+j*89
            if h>2:
                d.rounded_rectangle((bx,bottom-h,bx+73,bottom),radius=11,fill=color)
            if phase>.6:
                draw_text(d,(bx+7,bottom-h-50),str(v),38,'#FFFFFF',True)
        draw_text(d,(x-24,851),month,34,'#D8EEF5',True)
    # Totals reveal only after the three groups have had time to animate.
    reveal=1 if progress>=0.75 else 0
    d.rounded_rectangle((69,943,1011,1125),radius=25,fill='#123D4F',outline='#2B7A84',width=2)
    draw_text(d,(95,957),'3か月合計',36,'#BEE8EE',True)
    if reveal>0:
        for j,(name,color) in enumerate((("営業A",accent),("営業B",'#AEB9FF'))):
            x=111+j*453
            draw_text(d,(x,1016),name,31,'#D9F3F7')
            value=TOTALS[name]
            draw_text(d,(x+168,995),str(value),66,color,True)
    else:
        draw_text(d,(111,1015),'4月 → 5月 → 6月を確認',34,'#BCD5E2')
    draw_text(d,(84,1155),'※説明用の架空データ。実際のExcel操作録画ではありません。',24,'#A9C9D4')
    return im

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

def aac_hash(path):
    proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    h=hashlib.sha256()
    while True:
        chunk=proc.stdout.read(65536)
        if not chunk:break
        h.update(chunk)
    err=proc.stderr.read().decode('utf8','replace')
    if proc.wait():raise RuntimeError('AAC extract failed: '+err[-1000:])
    return h.hexdigest()

def render(source,output,report,genre='ai_work',synthetic=False):
    import cv2
    import numpy as np
    require_genre(genre)
    source,output,report=map(Path,(source,output,report))
    if source.resolve()==output.resolve():raise ValueError('Source and output must differ')
    cap=cv2.VideoCapture(str(source))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));w=int(cap.get(3));h=int(cap.get(4));fps=cap.get(5)
    if (w,h)!=(W,H) or abs(fps-FPS)>.01:raise ValueError('Source must be 1080x1920 at 30fps')
    if not synthetic and count!=691:raise ValueError('Unexpected private review source length')
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
            proc.stdin.write(frame.tobytes())
            written+=1
        proc.stdin.close();err=proc.stderr.read().decode('utf8','replace')
        if proc.wait():raise RuntimeError('Encoding failed: '+err[-2000:])
    finally:
        cap.release()
        if proc.poll() is None:proc.kill()
    if written!=count:raise RuntimeError('Frame count mismatch')
    input_audio=aac_hash(source);output_audio=aac_hash(output)
    p=probe(output)
    vs=next(s for s in p['streams'] if s['codec_type']=='video')
    aud=next(s for s in p['streams'] if s['codec_type']=='audio')
    if input_audio!=output_audio:raise RuntimeError('Narration AAC payload changed')
    if (vs['width'],vs['height'],vs['codec_name'])!=(W,H,'h264') or aud['codec_name']!='aac':raise RuntimeError('Unexpected codecs')
    data={'source_sha256':sha(source),'output_sha256':sha(output),'duration_s':float(p['format']['duration']),'resolution':[W,H],'fps':FPS,'frames':written,'changed_frames':[start,end],'genre':genre,'data':DATA,'totals':TOTALS,'audio_aac_sha256':output_audio,'audio_payload_identical':True,'caption_pixels_intentionally_untouched_from_y':ART_BOTTOM,'caption_visual_decoding':'MANUAL_REVIEW_REQUIRED','independent_japanese_asr':'UNVERIFIED','subtitle_semantic_timing':'UNVERIFIED','source_rights':'UNVERIFIED','employee_approval':False,'publication_approved':False,'synthetic_ci_only':bool(synthetic)}
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');p.add_argument('--synthetic',action='store_true')
    args=p.parse_args();print(json.dumps(render(args.source,args.output,args.report,args.genre,args.synthetic),ensure_ascii=False,indent=2))
