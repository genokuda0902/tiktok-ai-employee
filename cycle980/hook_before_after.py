#!/usr/bin/env python3
"""Review-only before/after visual hook using frames of an existing local video.

Does not create narration, publish assets, or claim real-world time savings.
Only ai_work source coordinates have been manually inspected; other genres fail closed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

FPS=30
WIDTH=1080
HEIGHT=1920
SAFE_Y=1440
HOOK_FRAMES=45
GENRES=('ai_work','finance','learning','health','travel','food','science','history','business','lifestyle')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'


def run(cmd, capture=False):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE if capture else None, stderr=subprocess.PIPE if capture else None)


def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()


def probe(path):
    obj=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels','-show_entries','format=duration','-of','json',str(path)],True).stdout)
    v=[x for x in obj['streams'] if x['codec_type']=='video']
    a=[x for x in obj['streams'] if x['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1:raise ValueError('Exactly one video and one audio track required')
    if (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'])!=(WIDTH,HEIGHT,'30/1'):raise ValueError('Source geometry unreviewed')
    n=int(v[0].get('nb_frames') or round(float(obj['format']['duration'])*FPS))
    if n<HOOK_FRAMES+1:raise ValueError('Source too short')
    return n,obj


def validate(genre, synthetic=False):
    if genre not in GENRES:raise ValueError('Unknown genre')
    if genre!='ai_work' and not synthetic:raise ValueError('Unreviewed genre layout: fail closed')


def frame_at(video, idx, out):
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),'-vf',f'select=eq(n\\,{idx})','-vsync','0','-frames:v','1',str(out)])
    with Image.open(out) as im:return im.convert('RGB').copy()


def fit_crop(im, box, size):
    im=im.crop(box)
    w,h=size
    s=max(w/im.width,h/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS)
    x=(im.width-w)//2;y=(im.height-h)//2
    return im.crop((x,y,x+w,y+h))


def render_frame(before, after, i):
    if not 0<=i<HOOK_FRAMES:raise ValueError('Invalid frame index')
    img=Image.new('RGB',(WIDTH,SAFE_Y),(6,14,31))
    d=ImageDraw.Draw(img)
    for y in range(0,SAFE_Y,36):d.line((0,y,WIDTH,y),fill=(10,24,43),width=1)
    fbig=ImageFont.truetype(FONT,67);fmid=ImageFont.truetype(FONT,37);fsmall=ImageFont.truetype(REG,28)
    d.rounded_rectangle((45,36,1035,120),radius=18,fill=(13,40,62),outline=(34,151,196),width=3)
    d.text((70,57),'AI仕事術 / BEFORE → AFTER',font=fsmall,fill=(161,233,249))
    d.text((55,153),'まだ手作業？',font=fbig,fill='white',stroke_width=1)
    d.text((56,249),'元データと照合できる形へ',font=fmid,fill=(109,234,226))
    # Split-screen: illustrative existing scene and Calc-derived fictional sample.
    bw,bh=470,790
    b=fit_crop(before,(30,140,1040,1280),(bw,bh))
    a=fit_crop(after,(40,155,1040,1290),(bw,bh))
    phase=i/(HOOK_FRAMES-1)
    if phase<.35:
        a=ImageEnhance.Brightness(a).enhance(.35+.65*phase/.35)
    elif phase<.72:
        b=ImageEnhance.Brightness(b).enhance(1-.38*(phase-.35)/.37)
    img.paste(b,(55,395));img.paste(a,(555,395))
    d=ImageDraw.Draw(img)
    d.rounded_rectangle((52,392,528,1188),radius=16,outline=(242,144,130),width=6)
    d.rounded_rectangle((552,392,1028,1188),radius=16,outline=(83,229,209),width=6)
    d.rounded_rectangle((69,410,309,479),radius=12,fill=(64,23,40))
    d.text((85,423),'BEFORE / イメージ',font=fsmall,fill=(255,219,218))
    d.rounded_rectangle((567,410,958,479),radius=12,fill=(8,72,69))
    d.text((581,423),'AFTER / 架空データ',font=fsmall,fill=(210,255,241))
    # An explicit reveal bar makes the change legible without implying actual performance.
    arrow_x=round(492+10*max(0,phase-.45))
    d.rounded_rectangle((arrow_x-15,772,arrow_x+90,857),radius=24,fill=(6,25,46),outline=(238,246,250),width=3)
    d.text((arrow_x+8,781),'→',font=ImageFont.truetype(FONT,51),fill=(245,250,255))
    d.rounded_rectangle((55,1230,1025,1350),radius=19,fill=(11,41,59),outline=(38,140,155),width=3)
    d.text((78,1253),'手作業の確認 → 表で検算・見直し',font=fmid,fill='white')
    d.rounded_rectangle((55,1373,1025,1387),radius=7,fill=(28,54,73))
    d.rounded_rectangle((55,1373,55+round(970*(i+1)/HOOK_FRAMES),1387),radius=7,fill=(84,234,210))
    return img


def render(source,output,work,genre='ai_work',synthetic=False):
    validate(genre,synthetic)
    source=Path(source);output=Path(output);work=Path(work)
    if not source.is_file():raise FileNotFoundError(source)
    count,_=probe(source)
    work.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
    before=frame_at(source,105,work/'before_source.png')
    after=frame_at(source,195,work/'after_source.png')
    frames=work/'frames';frames.mkdir(exist_ok=True)
    for i in range(HOOK_FRAMES):render_frame(before,after,i).save(frames/f'{i:03d}.png',compress_level=2)
    graph=f'[0:v][1:v]overlay=0:0:eof_action=pass:enable=\'lt(n,{HOOK_FRAMES})\'[v]'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate',str(FPS),'-start_number','0','-i',str(frames/'%03d.png'),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(count),'-c:a','copy','-movflags','+faststart',str(output)])
    n2,_=probe(output)
    if n2!=count:raise RuntimeError(f'Frame count changed {count}->{n2}')
    return {'source_sha256':sha(source),'output_sha256':sha(output),'frames':count,'hook_frames':HOOK_FRAMES,'caption_protected_y':SAFE_Y,'genre':genre,'review_only':True,'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for a in ('source','output','work'):p.add_argument('--'+a,required=True)
    p.add_argument('--genre',default='ai_work');p.add_argument('--synthetic',action='store_true')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.work,a.genre,a.synthetic),ensure_ascii=False,indent=2))
