#!/usr/bin/env python3
"""Render a review-only, genuinely screen-captured Calc UI scene.

The screen capture is local/private and is NEVER committed to GitHub.
This does not recover v33 or verify semantic Japanese speech alignment.
Only the inspected ai_work scene coordinates are allowed; other genres fail closed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
from PIL import Image, ImageDraw, ImageFont

FPS=30
START=174
END=261
SAFE_Y=1440
GENRES=('ai_work','finance','learning','health','travel','food','science','history','business','lifestyle')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def run(args):
    return subprocess.run(args,check=True,capture_output=True,text=True)

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def metadata(path):
    p=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate','-show_entries','format=duration','-of','json',str(path)]).stdout)
    video=[s for s in p['streams'] if s['codec_type']=='video']
    audio=[s for s in p['streams'] if s['codec_type']=='audio']
    return video,audio,p

def validate(genre,synthetic=False):
    if genre not in GENRES:raise ValueError('Unknown genre')
    if genre!='ai_work' and not synthetic:raise ValueError('Unreviewed genre: fail closed')

def artwork(gui,frame_index,synthetic=False):
    """Return 1080x1440 artwork only, keeping inherited caption area intact."""
    if not 0<=frame_index<END-START:raise ValueError('Frame out of range')
    if gui.width<600 or gui.height<400:raise ValueError('GUI capture too small')
    canvas=Image.new('RGB',(1080,SAFE_Y),(5,20,38));d=ImageDraw.Draw(canvas)
    bold=ImageFont.truetype(FONT,55);mid=ImageFont.truetype(FONT,39);small=ImageFont.truetype(REG,28)
    d.rounded_rectangle((44,36,1036,118),radius=18,fill=(12,44,66),outline=(45,184,199),width=3)
    d.text((69,53),'REAL GUI / LibreOffice Calc',font=small,fill=(166,244,244))
    d.text((51,156),'数式を入力して、結果を検算',font=bold,fill='white')
    d.text((53,247),'架空データ｜実際の画面操作を録画',font=mid,fill=(126,239,225))
    # Crop only the GUI from a synthetic, freshly-created workbook.
    x0,y0,x1,y1=(57,148,min(1172,gui.width),min(695,gui.height))
    if x1-x0<500 or y1-y0<300:raise ValueError('Unreviewed screen geometry')
    crop=gui.crop((x0,y0,x1,y1));crop.thumbnail((968,625),Image.Resampling.LANCZOS)
    px=54+(972-crop.width)//2;py=357+(625-crop.height)//2
    d.rounded_rectangle((44,346,1036,1002),radius=22,fill=(235,244,248),outline=(69,183,191),width=5)
    canvas.paste(crop,(px,py))
    d=ImageDraw.Draw(canvas)
    phase=frame_index/(END-START-1)
    step='① 営業A  SUM(B2:B4)' if phase<.49 else '② 営業B  SUM(C2:C4)'
    d.rounded_rectangle((52,1028,1028,1138),radius=18,fill=(14,49,72),outline=(38,125,149),width=3)
    d.text((75,1048),step,font=mid,fill='white')
    d.rounded_rectangle((52,1160,527,1315),radius=17,fill=(14,78,75),outline=(77,218,191),width=3)
    d.rounded_rectangle((551,1160,1028,1315),radius=17,fill=(17,65,88),outline=(72,185,224),width=3)
    d.text((77,1181),'営業A',font=small,fill=(198,248,235));d.text((320,1183),'46',font=bold,fill='white')
    d.text((575,1181),'営業B',font=small,fill=(200,236,255));d.text((817,1183),'29',font=bold,fill='white')
    d.text((58,1351),'※ 実在の業務実績ではありません',font=small,fill=(187,206,218))
    d.rounded_rectangle((53,1404,1027,1417),radius=6,fill=(24,60,76))
    d.rounded_rectangle((53,1404,53+int(974*(frame_index+1)/(END-START)),1417),radius=6,fill=(89,232,214))
    return canvas

def render(source,screen,output,work,genre='ai_work',synthetic=False):
    validate(genre,synthetic)
    source,screen,output,work=map(Path,(source,screen,output,work))
    for p in (source,screen):
        if not p.is_file():raise FileNotFoundError(p)
    v,a,_=metadata(source)
    if len(v)!=1 or len(a)!=1 or (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('Source not 1080x1920/30fps with audio')
    n=int(v[0].get('nb_frames') or 0)
    if n<=END:raise ValueError('Source too short')
    cap=cv2.VideoCapture(str(screen))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if count<END-START:raise ValueError('Screen recording too short')
    work.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
    frames=work/'frames';frames.mkdir(exist_ok=True)
    for i in range(END-START):
        idx=round((.12+.83*i/(END-START-1))*(count-1))
        cap.set(cv2.CAP_PROP_POS_FRAMES,idx);ok,f=cap.read()
        if not ok:raise RuntimeError(f'Cannot read screen frame {idx}')
        gui=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
        artwork(gui,i,synthetic).save(frames/f'{i:03d}.png',compress_level=3)
    cap.release()
    art=work/'art.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','30','-i',str(frames/'%03d.png'),'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(art)])
    # Overlay only upper artwork for frames 174..260; original Japanese captions and AAC untouched.
    graph="[1:v]setpts=PTS-STARTPTS+5.8/TB[art];[0:v][art]overlay=0:0:eof_action=pass:enable='between(n,174,260)'[v]"
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(art),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30','-frames:v',str(n),'-c:a','copy','-movflags','+faststart',str(output)])
    v2,a2,_=metadata(output)
    if int(v2[0].get('nb_frames') or 0)!=n or a2[0]['codec_name']!='aac':raise RuntimeError('Output stream QA failed')
    return {'source_sha256':sha(source),'output_sha256':sha(output),'frames':n,'replaced_frames':END-START,'start_frame':START,'end_exclusive':END,'caption_protected_y':SAFE_Y,'genre':genre,'review_only':True,'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('source','screen','output','work'):p.add_argument('--'+key,required=True)
    p.add_argument('--genre',default='ai_work');p.add_argument('--synthetic',action='store_true')
    a=p.parse_args();print(json.dumps(render(a.source,a.screen,a.output,a.work,a.genre,a.synthetic),ensure_ascii=False,indent=2))
