#!/usr/bin/env python3
"""Review-only three-stage focus for a Writer-like document, not original v33.

Highlights source text in reading order; does not replace source text or alter
Japanese narration/subtitles. The underlying screenshot rights are inherited
and NOT approved for publication. No private assets are stored in this module.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = {
    'ai':'#36d8cd','business':'#6dd1f5','money':'#e8c16b',
    'learning':'#9abaff','health':'#75d5a7','food':'#efb97e',
    'travel':'#80c8e8','beauty':'#efafd2','career':'#a2a5ff','life':'#a7dfb0',
}
FPS=30
# Within the existing Writer page only; header/chapter bar and caption remain unchanged.
X,Y,W,H=104,551,754,260
ROWS=((15,14,692,69),(15,95,692,69),(15,176,692,69))
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def probe(path):
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(s for s in data['streams'] if s['codec_type']=='video')
    a=next(s for s in data['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],int(v['width']),int(v['height']),v['avg_frame_rate'])!=('h264',1080,1920,'30/1'):
        raise ValueError('Expected H264 1080x1920 30fps')
    if (a['codec_name'],int(a['sample_rate']))!=('aac',48000):
        raise ValueError('Expected AAC 48kHz')
    return float(data['format']['duration']),int(v.get('nb_frames') or round(float(data['format']['duration'])*FPS))


def validate(m,source,duration):
    if (m.get('policy')!=POLICY or m.get('asset_approval')!='review_only_no_publication'
            or m.get('manual_post_only') is not True):
        raise ValueError('Fail closed: publication policy')
    if m.get('source_sha256')!=sha256(source):raise ValueError('Source SHA mismatch')
    if m.get('genre') not in GENRES:raise ValueError('Unsupported genre')
    if m.get('layout_id')!='writer_three_rows_v1':raise ValueError('Unsupported layout; requires manual layout QA')
    window=m.get('window')
    if not isinstance(window,list) or len(window)!=2 or any(type(x) not in (int,float) for x in window):
        raise ValueError('Invalid time window')
    start,end=map(float,window)
    if not (0<=start<end<=duration and 2.2<=end-start<=2.7):raise ValueError('Unsafe time window')
    if (X<50 or X+W>940 or Y<500 or Y+H>850):raise ValueError('Protected area overlap')
    return start,end


def stage(index,count):
    return min(2, 3*index//max(count,1))


def overlay_frame(genre,index,count):
    """Transparent outlines only; never obscures the source document text."""
    accent=tuple(bytes.fromhex(GENRES[genre][1:]))
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    selected=stage(index,count)
    for k,(x,y,w,h) in enumerate(ROWS):
        if k>selected:continue
        active=(k==selected)
        strength=min(1.0,(index%max(1,count//3)+1)/6) if active else 0.38
        alpha=int((228 if active else 90)*strength)
        color=accent+(alpha,)
        # Thin border, no text fill. Draw glow outside the border, not on glyphs.
        d.rounded_rectangle((x,y,x+w,y+h),radius=11,outline=accent+(int(alpha*.35),),width=8)
        d.rounded_rectangle((x+2,y+2,x+w-2,y+h-2),radius=10,outline=color,width=3)
        # Number chip sits to the right of text in the page margin.
        cx=x+w-53
        d.rounded_rectangle((cx,y+12,cx+39,y+53),radius=8,fill=(6,35,49,int(205*strength)),outline=color,width=2)
        d.text((cx+10,y+17),str(k+1),font=ImageFont.truetype(FONT,24),fill=(246,252,252,int(240*strength)))
    # Smooth fade in/out to avoid a visible pop at chapter cuts.
    fade=min(1.0,(index+1)/6,(count-index)/6)
    if fade<1:im.putalpha(im.getchannel('A').point(lambda a:int(a*fade)))
    return im


def render(source,output,manifest,workdir):
    source,output,manifest,workdir=map(Path,(source,output,manifest,workdir))
    if source.resolve()==output.resolve():raise ValueError('Source must remain untouched')
    m=json.loads(manifest.read_text(encoding='utf-8'))
    duration,frames=probe(source);start,end=validate(m,source,duration)
    workdir.mkdir(parents=True,exist_ok=True)
    folder=workdir/'overlay_frames';folder.mkdir(exist_ok=True)
    n=round((end-start)*FPS)
    for i in range(n):overlay_frame(m['genre'],i,n).save(folder/f'{i:04d}.png',compress_level=3)
    filt=f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start}/TB[ov];[0:v][ov]overlay={X}:{Y}:format=auto:eof_action=pass:shortest=0[v]'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-i',str(folder/'%04d.png'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-threads','4','-c:a','copy','-t',f'{duration:.6f}','-movflags','+faststart',str(output)],check=True)
    d,f=probe(output)
    if abs(d-duration)>.05 or f!=frames:raise RuntimeError('Duration/frame count mismatch')
    report={'policy':POLICY,'source_sha256':sha256(source),'output_sha256':sha256(output),'duration':d,'frames':f,'window':[start,end],'highlight_frames':n,'genre':m['genre'],'stages':['目的','条件','形式'],'media_rights':'INHERITED_SOURCE_UNVERIFIED','Japanese_ASR':'NOT_VERIFIED','publication_approved':False}
    (workdir/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','workdir'):p.add_argument('--'+k,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.workdir),ensure_ascii=False,indent=2))
