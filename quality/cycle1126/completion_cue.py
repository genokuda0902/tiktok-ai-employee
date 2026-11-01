#!/usr/bin/env python3
"""Review-only animated completion cue for 10-genre vertical video.

Original reimplementation, NOT original v33. No upload/posting. Source media
must be local, pinned and explicitly marked private-review-only.
"""
from __future__ import annotations
import argparse, hashlib, json, math, re, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
APPROVAL='review_only_no_public_rights_claim'
FONTS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc','/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc')

def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(f'{cmd[0]} failed: '+p.stderr.decode('utf-8','replace')[-1800:])
    return p.stdout

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_hash(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','adts','-'])).hexdigest()

def media_info(path):
    m=probe(path);v=[x for x in m['streams'] if x['codec_type']=='video'];a=[x for x in m['streams'] if x['codec_type']=='audio'];s=[x for x in m['streams'] if x['codec_type']=='subtitle']
    if len(v)!=1 or len(a)!=1 or s:raise ValueError('require exactly one video/audio and zero soft subtitles')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac' or int(a[0]['sample_rate'])!=48000:raise ValueError('H264/AAC 48kHz required')
    num,den=map(int,v[0]['avg_frame_rate'].split('/'))
    if not den or abs(num/den-30)>.001:raise ValueError('30fps required')
    return int(v[0]['width']),int(v[0]['height']),int(v[0].get('nb_frames') or round(float(m['format']['duration'])*30)),float(m['format']['duration'])

def validate(m,source_sha,width,height,duration):
    if set(m)!={'policy','asset_approval','source_sha256','genre','cue'}:raise ValueError('unexpected manifest keys')
    if m['policy']!=POLICY or m['asset_approval']!=APPROVAL or m['source_sha256']!=source_sha:raise ValueError('not pinned or not review-only')
    if m['genre'] not in GENRES:raise ValueError('genre not supported')
    cue=m['cue']
    if set(cue)!={'start','switch','end','steps'} or len(cue['steps'])!=2:raise ValueError('two completion stages required')
    start,switch,end=map(float,(cue['start'],cue['switch'],cue['end']))
    if not (0<=start<switch<end<=duration and end-start<=3.5 and switch-start>=.25 and end-switch>=.25):raise ValueError('invalid cue times')
    if not all(abs(t*30-round(t*30))<.02 for t in (start,switch,end)):raise ValueError('cue times must align with 30fps')
    for step in cue['steps']:
        if set(step)!={'rect','label'}:raise ValueError('bad step fields')
        label=step['label']
        if not isinstance(label,str) or not 3<=len(label)<=18 or '\n' in label or re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\b0\d{9,10}\b',label):raise ValueError('unsafe label')
        rect=step['rect']
        if not isinstance(rect,list) or len(rect)!=4 or not all(isinstance(z,(int,float)) and math.isfinite(z) for z in rect):raise ValueError('bad rect')
        x,y,w,h=rect
        if not (0<=x<1 and 0<=y<.7 and .15<=w<=.6 and .035<=h<=.15 and x+w<=.99 and y+h<=.72):raise ValueError('cue outside upper safe area')
        if w*width<160 or h*height<50:raise ValueError('cue too small to read')
    return start,switch,end

def font(size):
    for path in FONTS:
        if Path(path).exists():return ImageFont.truetype(path,size)
    raise FileNotFoundError('Noto CJK font required; do not silently substitute missing Japanese glyphs')

def smooth(x):
    x=max(0,min(1,x));return x*x*(3-2*x)

def overlay_frame(width,height,steps,t,start,switch,end):
    im=Image.new('RGBA',(width,height));d=ImageDraw.Draw(im)
    active=0 if t<switch else 1
    phase_start=start if active==0 else switch
    phase_end=switch if active==0 else end
    a=smooth((t-phase_start)/.22)*smooth((phase_end-t)/.17)
    if a<=.005:return im
    x,y,w,h=steps[active]['rect'];x,y,w,h=(round(x*width),round(y*height),round(w*width),round(h*height))
    pulse=1+0.12*math.sin((t-phase_start)*math.pi*5)
    line=max(3,round(width*.006*pulse));radius=max(10,round(height*.012))
    # Darkened active step, cyan focus and a visible completion dot; no subtitle occlusion.
    d.rounded_rectangle((x,y,x+w,y+h),radius=radius,fill=(5,79,91,round(225*a)),outline=(67,249,222,round(245*a)),width=line)
    label=steps[active]['label']
    for size in range(max(20,round(width*.034)),13,-1):
        face=font(size);box=d.textbbox((0,0),label,font=face);tw=box[2]-box[0]
        if tw<=w-40:break
    else:raise ValueError('label does not fit focus button')
    d.text((x+18,y+(h-(box[3]-box[1]))//2-4),label,font=face,fill=(250,255,255,round(255*a)))
    cx=x+w-24;cy=y+16;rr=7
    d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=(107,255,212,round(255*a)))
    return im

def export(source,output,manifest_path,report):
    source,output,manifest_path,report=(Path(x).resolve() for x in (source,output,manifest_path,report))
    if len({source,output,manifest_path,report})!=4:raise ValueError('paths must differ')
    if output.exists() or report.exists():raise FileExistsError('do not overwrite artifacts')
    if not source.is_file() or not manifest_path.is_file():raise FileNotFoundError('missing source or manifest')
    src_hash=sha(source);w,h,frames,duration=media_info(source)
    m=json.loads(manifest_path.read_text(encoding='utf-8'));start,switch,end=validate(m,src_hash,w,h,duration)
    output.parent.mkdir(parents=True,exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='cue_') as td:
            td=Path(td);n=round((end-start)*30)
            for i in range(n):
                t=start+i/30
                overlay_frame(w,h,m['cue']['steps'],t,start,switch,end).save(td/f'frame_{i:04d}.png',compress_level=1)
            flt=f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start}/TB[ov];[0:v][ov]overlay=0:0:format=auto:repeatlast=0:eof_action=pass[v]'
            run(['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-i',str(source),'-framerate','30','-i',str(td/'frame_%04d.png'),'-filter_complex',flt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-frames:v',str(frames),'-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)])
        w2,h2,f2,d2=media_info(output)
        if (w2,h2,f2)!=(w,h,frames) or abs(d2-duration)>.05:raise AssertionError('video geometry changed')
        if audio_hash(source)!=audio_hash(output):raise AssertionError('AAC elementary stream changed')
        run(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'])
        data={'policy':POLICY,'genre':m['genre'],'source_sha256':src_hash,'output_sha256':sha(output),'dimensions':[w,h],'fps':30,'frames':f2,'duration':d2,'cue_seconds':[start,switch,end],'audio_bitstream_unchanged':True,'full_decode':'PASS','soft_subtitles':0,'burned_subtitles':'SOURCE_RETAINED_REENCODED','independent_japanese_asr':'NOT_VERIFIED','human_approval':False}
        report.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return data
    except BaseException:
        output.unlink(missing_ok=True)
        raise

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','report'):p.add_argument('--'+k,required=True,type=Path)
    args=p.parse_args();print(json.dumps(export(args.source,args.output,args.manifest,args.report),ensure_ascii=False))
