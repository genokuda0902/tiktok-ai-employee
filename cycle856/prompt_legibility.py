"""cycle856: mobile-readable local prompt-demo animation, review only.

Creates no actual AI requests; all media stays local. Source MP4 is a rights-unverified
private review artifact. Never commit the source video or derived frames.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
PALETTES = {g: (35+(i*9)%85, 191-(i*5)%65, 219-(i*7)%60) for i,g in enumerate(GENRES)}
POLICY = {'review_only':True,'publication_approved':False,'automatic_posting':False,
          'external_upload':False,'source_rights_reviewed':False,
          'contains_personal_data':False,'fictional_workflow_example':True}
PANEL = (86,476,994,1234)
# Scene 04 original offline mock extends beyond generic picture inset.
# Cover its full bounds to avoid leaving duplicate top/bottom UI strips.
SCENE_COVER = (44,330,1036,1420)
WINDOW = (251,336)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
DEFAULT_CONTENT = {
    'lines':['この売上データを整理して','重要な点を3つ教えて'],
    'chips':['対象：売上データ','目的：整理','出力：要点3つ'],
}

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def stream_info(path):
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))
    v=next((x for x in p['streams'] if x['codec_type']=='video'),None)
    a=next((x for x in p['streams'] if x['codec_type']=='audio'),None)
    return v,a

def validate_content(content):
    if not isinstance(content,dict) or set(content)!={'lines','chips'}:raise ValueError('exact lines/chips required')
    if not isinstance(content['lines'],list) or len(content['lines'])!=2:raise ValueError('two lines required')
    if not isinstance(content['chips'],list) or len(content['chips'])!=3:raise ValueError('three chips required')
    for s in content['lines']:
        if not isinstance(s,str) or not 1<=len(s)<=16 or any(ord(c)<32 for c in s):
            raise ValueError('line must be 1..16 printable characters')
    for s in content['chips']:
        if not isinstance(s,str) or not 1<=len(s)<=12 or any(ord(c)<32 for c in s):
            raise ValueError('chip must be 1..12 printable characters')
    return content

def validate(source,output,manifest,genre,window,content):
    source=Path(source);output=Path(output)
    if genre not in GENRES or len(GENRES)!=10:raise ValueError('unsupported genre')
    validate_content(content)
    if not source.is_file():raise FileNotFoundError('source MP4 missing')
    if manifest!={**POLICY,'source_sha256':sha256(source)}:raise ValueError('review policy or source SHA mismatch')
    if source.resolve()==output.resolve() or output.exists():raise ValueError('no overwrite')
    v,a=stream_info(source)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',1080,1920,'30/1','aac'):
        raise ValueError('requires 1080x1920 H264 30fps with AAC')
    n=int(v['nb_frames'])
    if len(window)!=2 or any(type(x)!=int for x in window) or not 0<=window[0]<window[1]<=n or window[1]-window[0]<30:
        raise ValueError('invalid scene window')
    if not Path(FONT).exists():raise FileNotFoundError('Noto CJK font required')
    return n

def font(size):return ImageFont.truetype(FONT,size)

def visible_chars(frame,total,content):
    if not 0<=frame<total:raise ValueError('bad frame')
    text=''.join(content['lines'])
    # Typing begins immediately and ends with 15 frames for a held, readable result.
    count=min(len(text),int(len(text)*min(1,(frame+1)/max(1,total-15))))
    return count

def draw_panel(frame,total,genre,content=DEFAULT_CONTENT):
    validate_content(content)
    if genre not in GENRES:raise ValueError('unsupported genre')
    if not 0<=frame<total or total<30:raise ValueError('bad animation position')
    accent=PALETTES[genre]
    im=Image.new('RGB',(908,758),(6,18,31));d=ImageDraw.Draw(im)
    # Deliberately original/offline UI: not a brand impersonation or real AI submission.
    d.rounded_rectangle((18,17,890,741),radius=30,fill=(9,31,48),outline=accent,width=3)
    d.rounded_rectangle((43,39,430,90),radius=15,fill=accent)
    d.text((236,65),'OFFLINE DEMO / 04',font=font(25),anchor='mm',fill=(4,22,33))
    d.text((48,122),'指示は短く、具体的に',font=font(52),fill=(246,251,255))
    d.text((51,193),'架空データを使った入力例',font=font(28),fill=(166,211,222))
    d.rounded_rectangle((42,254,865,551),radius=27,fill=(244,249,249))
    d.text((72,275),'指示入力',font=font(28),fill=(22,69,77))
    shown=visible_chars(frame,total,content)
    lines=content['lines']
    first=min(shown,len(lines[0]));second=max(0,shown-len(lines[0]))
    d.text((73,339),lines[0][:first],font=font(51),fill=(12,40,52))
    if second:d.text((73,422),lines[1][:second],font=font(51),fill=(12,40,52))
    # Caret is attached to the typing line and never leaves the prompt box.
    caret_line=lines[1][:second] if second else lines[0][:first]
    caret_y=423 if second else 340
    caret_x=73+d.textlength(caret_line,font=font(51))+8
    if frame%18<12:d.line((caret_x,caret_y,caret_x,caret_y+59),fill=accent,width=5)
    # Three short structured constraints are progressively disclosed.
    for i,label in enumerate(content['chips']):
        x=45+i*276
        active=frame>=int(total*(i+1)/5)
        fill=(18,78,92) if active else (20,44,58)
        outline=accent if active else (44,74,85)
        d.rounded_rectangle((x,584,x+263,650),radius=18,fill=fill,outline=outline,width=2)
        d.text((x+131,617),label,font=font(26),anchor='mm',fill=(250,252,253) if active else (126,161,170))
    d.rounded_rectangle((49,674,859,720),radius=12,fill=(9,51,62))
    d.text((454,697),'ローカル再現UI ／ 実際のAI送信なし',font=font(24),anchor='mm',fill=(195,231,233))
    return im

def compose_frame(frame,panel):
    if frame.shape!=(1920,1080,3) or panel.size!=(908,758):raise ValueError("frame or panel geometry")
    x0,y0,x1,y1=SCENE_COVER
    frame[y0:y1,x0:x1]=(31,18,6)
    fitted=cv2.resize(np.asarray(panel), (970,811), interpolation=cv2.INTER_AREA)
    x=x0+((x1-x0)-970)//2
    y=y0+((y1-y0)-811)//2
    frame[y:y+811,x:x+970]=cv2.cvtColor(fitted,cv2.COLOR_RGB2BGR)
    return frame

def render(source,output,manifest,genre='ai_work',window=WINDOW,content=DEFAULT_CONTENT):
    n=validate(source,output,manifest,genre,window,content)
    cap=cv2.VideoCapture(str(source))
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s','1080x1920','-r','30','-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-c:a','copy',
         '-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    changed=0
    try:
        for i in range(n):
            ok,frame=cap.read()
            if not ok:raise RuntimeError('source frame truncated')
            if window[0]<=i<window[1]:
                panel=draw_panel(i-window[0],window[1]-window[0],genre,content)
                frame=compose_frame(frame,panel)
                changed+=1
            p.stdin.write(frame.tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait()!=0:raise RuntimeError('FFmpeg encode: '+err[-1000:])
    except Exception:
        p.kill();p.wait();Path(output).unlink(missing_ok=True);raise
    finally:cap.release()
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    v,a=stream_info(output)
    if int(v['nb_frames'])!=n or a['codec_name']!='aac':raise RuntimeError('output stream invalid')
    return {'cycle':856,'genre':genre,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'frames':n,'window':list(window),'changed_frames':changed,
            'prompt_font_px':51,'prior_prompt_font_px_estimate':33,
            'full_av_decode':True,'independent_japanese_asr_verified':False,
            'semantic_subtitle_sync_verified':False,'source_rights_reviewed':False,
            'smartphone_playback_verified':False,'publication_approved':False,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('source','output','manifest','report'):p.add_argument('--'+name,required=True)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--window',nargs=2,type=int,default=list(WINDOW))
    p.add_argument('--content-json')
    a=p.parse_args()
    content=json.loads(Path(a.content_json).read_text(encoding='utf-8')) if a.content_json else DEFAULT_CONTENT
    report=render(a.source,a.output,json.loads(Path(a.manifest).read_text(encoding='utf-8')),
                  a.genre,tuple(a.window),content)
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
