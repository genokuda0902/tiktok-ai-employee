#!/usr/bin/env python3
"""Review-only 2-stage visual focus overlay for 10 genre short videos.

Reimplementation, not original v33 code. No media is committed or published.
Independent Japanese ASR and employee/rights approval remain required.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
APPROVAL = 'review_only_no_public_rights_claim'
FONT_PATHS = ('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
              '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
              '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')


def execute(argv):
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(f"command failed ({p.returncode}): {argv[0]} {p.stderr.decode('utf-8', 'replace')[-1200:]}")
    return p.stdout


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def probe(path):
    return json.loads(execute(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def stream_digest(path, stream):
    ext = 'h264' if stream == 'v' else 'adts'
    return hashlib.sha256(execute(['ffmpeg','-v','error','-i',str(path),'-map',f'0:{stream}:0','-c','copy','-f',ext,'-'])).hexdigest()


def verify_media(meta):
    v=[s for s in meta['streams'] if s['codec_type']=='video']
    a=[s for s in meta['streams'] if s['codec_type']=='audio']
    subs=[s for s in meta['streams'] if s['codec_type']=='subtitle']
    if len(v)!=1 or len(a)!=1 or subs: raise ValueError('one video, one audio, zero subtitle tracks required')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac':raise ValueError('H264/AAC required')
    if int(a[0]['sample_rate'])!=48000:raise ValueError('48kHz AAC required')
    width,height=int(v[0]['width']),int(v[0]['height'])
    num,den=map(int,v[0]['avg_frame_rate'].split('/'))
    if den==0 or abs(num/den-30)>.01:raise ValueError('30fps required')
    return width,height,int(v[0].get('nb_frames') or round(float(meta['format']['duration'])*30)),float(meta['format']['duration'])


def safe_label(label):
    if not isinstance(label,str) or not 2<=len(label)<=24 or '\n' in label:
        raise ValueError('bad label length')
    if re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\b0\d{9,10}\b',label):
        raise ValueError('potential PII in label')
    return label


def validate_manifest(m,source_hash,width,height,duration):
    if set(m)!={'policy','asset_approval','source_sha256','genre','focus_scene'}:raise ValueError('manifest fields must be exact')
    if m['policy']!=POLICY or m['asset_approval']!=APPROVAL or m['source_sha256']!=source_hash:
        raise ValueError('not pinned / no review-only approval')
    if m['genre'] not in GENRES:raise ValueError('unknown genre')
    s=m['focus_scene']
    if set(s)!={'start','split','end','focuses'} or len(s['focuses'])!=2:raise ValueError('two-stage focus required')
    start,split,end=map(float,(s['start'],s['split'],s['end']))
    if not (0<=start<split<end<=duration):raise ValueError('focus timing out of range')
    if end-start>8:raise ValueError('focus scene too long')
    for f in s['focuses']:
        if set(f)!={'label','rect','badge_xy'}:raise ValueError('bad focus fields')
        safe_label(f['label'])
        x,y,w,h=f['rect']
        if not all(isinstance(v,int) for v in (x,y,w,h)) or w<32 or h<20 or x<0 or y<0 or x+w>width or y+h>int(height*.70):
            raise ValueError('focus box outside safe upper image area')
        bx,by=f['badge_xy']
        if not all(isinstance(v,int) for v in (bx,by)) or bx<0 or by<0 or bx>width-250 or by>int(height*.68):
            raise ValueError('badge outside safe upper image area')
    return start,split,end


def font(size):
    for path in FONT_PATHS:
        if Path(path).exists():return ImageFont.truetype(path,size)
    raise FileNotFoundError('Noto CJK or DejaVu font required; do not silently omit Japanese')


def make_overlay(focus,width,height,destination,accent):
    im=Image.new('RGBA',(width,height),(0,0,0,0))
    d=ImageDraw.Draw(im)
    x,y,w,h=focus['rect']
    d.rounded_rectangle((x-10,y-10,x+w+10,y+h+10),radius=18,outline=accent+(65,),width=12)
    d.rounded_rectangle((x-4,y-4,x+w+4,y+h+4),radius=10,outline=accent+(230,),width=6)
    bx,by=focus['badge_xy']
    label=focus['label']
    face=font(max(22,round(width*0.033)))
    bbox=d.textbbox((0,0),label,font=face)
    tw=bbox[2]-bbox[0]
    # Opaque wide banner masks any pre-existing animated hint, including stale/wrong formulas.
    badge_w=min(width-bx-12,round(width*.85))
    if tw+50>badge_w:raise ValueError('focus label exceeds safe banner width')
    d.rounded_rectangle((bx,by,bx+badge_w,by+76),radius=18,fill=(4,20,38,255),outline=accent+(240,),width=3)
    d.text((bx+25,by+11),label,font=face,fill=(248,252,255,255),stroke_width=0)
    im.save(destination)


def export(source,output,manifest_path,report):
    source,output,manifest_path,report=map(lambda p:Path(p).resolve(),(source,output,manifest_path,report))
    if len({source,output,manifest_path,report})!=4:raise ValueError('all paths must differ')
    if output.exists() or report.exists():raise FileExistsError('refuse to overwrite review artifacts')
    if not source.is_file() or not manifest_path.is_file():raise FileNotFoundError('missing local source/manifest')
    src_hash=digest(source)
    original=probe(source)
    width,height,frames,duration=verify_media(original)
    m=json.loads(manifest_path.read_text(encoding='utf-8'))
    start,split,end=validate_manifest(m,src_hash,width,height,duration)
    output.parent.mkdir(parents=True,exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='focus_') as temp:
            one=Path(temp)/'one.png';two=Path(temp)/'two.png'
            make_overlay(m['focus_scene']['focuses'][0],width,height,one,(34,221,208))
            make_overlay(m['focus_scene']['focuses'][1],width,height,two,(255,189,67))
            flt=(f'[0:v][1:v]overlay=0:0:format=auto:enable=between(t\\,{start}\\,{split-0.001:.3f})[v1];'
                 f'[v1][2:v]overlay=0:0:format=auto:enable=between(t\\,{split}\\,{end})[v]')
            execute(['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-i',str(source),
                     '-loop','1','-framerate','30','-i',str(one),'-loop','1','-framerate','30','-i',str(two),
                     '-filter_complex',flt,'-map','[v]','-map','0:a:0','-c:v','libx264',
                     '-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-frames:v',str(frames),
                     '-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)])
        new=probe(output)
        w2,h2,fr2,d2=verify_media(new)
        if (w2,h2,fr2)!=(width,height,frames) or abs(d2-duration)>.05:
            raise AssertionError('render changed dimensions, frames or duration')
        if stream_digest(source,'a')!=stream_digest(output,'a'):
            raise AssertionError('audio elementary stream changed')
        execute(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'])
        result={'policy':POLICY,'genre':m['genre'],'source_sha256':src_hash,'output_sha256':digest(output),
                'duration_seconds':d2,'frames':fr2,'width':w2,'height':h2,'fps':30,
                'focus_times':[start,split,end],'audio_elementary_unchanged':True,
                'full_decode':'PASS','soft_subtitles':0,'burned_subtitles':'SOURCE_VISUALS_RETAINED_REENCODED',
                'independent_japanese_asr':'NOT_VERIFIED','publication_approved':False}
        report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return result
    except BaseException:
        output.unlink(missing_ok=True)
        raise


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for n in ('source','output','manifest','report'):ap.add_argument('--'+n,required=True,type=Path)
    a=ap.parse_args()
    print(json.dumps(export(a.source,a.output,a.manifest,a.report),ensure_ascii=False))
