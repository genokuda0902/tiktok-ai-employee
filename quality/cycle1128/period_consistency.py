#!/usr/bin/env python3
"""Private review-only correction of a fictional data period label.

A reusable fail-closed period consistency gate for ten genres. This is a
reimplementation and never validates source-media rights or speech semantics.
"""
import argparse, hashlib, json, re, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(p.stderr.decode('utf-8','replace')[-1600:])
    return p.stdout

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def audio_hash(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','adts','-'])).hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def inspect(path):
    p=probe(path);v=[x for x in p['streams'] if x['codec_type']=='video'];a=[x for x in p['streams'] if x['codec_type']=='audio'];s=[x for x in p['streams'] if x['codec_type']=='subtitle']
    if len(v)!=1 or len(a)!=1 or s:raise ValueError('one video, one audio, no soft subtitles required')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac' or a[0]['sample_rate']!='48000':raise ValueError('H264/AAC48 required')
    if (v[0]['width'],v[0]['height']) not in [(1080,1920),(540,960)]:raise ValueError('unsupported geometry')
    if v[0]['avg_frame_rate']!='30/1':raise ValueError('30fps required')
    return v[0]['width'],v[0]['height'],int(v[0]['nb_frames']),float(p['format']['duration'])

def validate(m,source_sha,video_duration):
    if set(m)!={'policy','asset_approval','source_sha256','genre','period','patch'}:raise ValueError('manifest schema mismatch')
    if m['policy']!=POLICY or m['asset_approval']!='private_review_only' or m['source_sha256']!=source_sha:raise ValueError('approval or source hash mismatch')
    if m['genre'] not in GENRES:raise ValueError('unsupported genre')
    period=m['period']
    if set(period)!={'month_labels','claimed_month_count','corrected_month_count'}:raise ValueError('period schema mismatch')
    labels=period['month_labels']
    if not isinstance(labels,list) or len(labels)<2 or len(labels)>12 or len(set(labels))!=len(labels) or any(not re.fullmatch(r'(?:1[0-2]|[1-9])月',x) for x in labels):raise ValueError('invalid months')
    if period['corrected_month_count']!=len(labels) or period['claimed_month_count']==len(labels):raise ValueError('no verified inconsistency')
    patch=m['patch']
    if set(patch)!={'start_frame','end_frame','digit_bbox','digit_origin','replacement'}:raise ValueError('patch schema mismatch')
    if patch['replacement']!=str(len(labels)) or not re.fullmatch('[0-9]{1,2}',patch['replacement']):raise ValueError('invalid replacement')
    start,end=patch['start_frame'],patch['end_frame']
    if not isinstance(start,int) or not isinstance(end,int) or not (0<=start<end<=round(video_duration*30) and end-start<=120):raise ValueError('unsafe patch range')
    x0,y0,x1,y1=patch['digit_bbox'];x,y=patch['digit_origin']
    if not (0<=x0<x1<=1080 and 0<=y0<y1<=1200 and 0<=x<=x1 and 0<=y<=y1):raise ValueError('unsafe patch geometry')
    if x1-x0>100 or y1-y0>70:raise ValueError('patch exceeds single-digit geometry')
    return start,end

def overlay(width,height,m):
    scale=width/1080;im=Image.new('RGBA',(width,height));d=ImageDraw.Draw(im)
    b=[round(z*scale) for z in m['patch']['digit_bbox']];xy=tuple(round(z*scale) for z in m['patch']['digit_origin'])
    d.rectangle(b,fill=(11,43,64,255))
    if not Path(FONT).exists():raise FileNotFoundError('Japanese Noto font required')
    f=ImageFont.truetype(FONT,round(30*scale))
    d.text(xy,m['patch']['replacement'],font=f,fill=(198,223,235,255))
    return im

def render(source,out,manifest,qa):
    source,out,manifest,qa=map(lambda p:Path(p).resolve(),(source,out,manifest,qa))
    if len({source,out,manifest,qa})!=4 or out.exists() or qa.exists():raise ValueError('unsafe overwrite/path')
    w,h,frames,dur=inspect(source);m=json.loads(manifest.read_text(encoding='utf8'));start,end=validate(m,sha(source),dur)
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='period_fix_') as tmp:
        tmp=Path(tmp)
        frame=overlay(w,h,m)
        for i in range(end-start):frame.save(tmp/f'frame_{i:04d}.png',compress_level=1)
        filt=f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start}/30/TB[ov];[0:v][ov]overlay=0:0:format=auto:repeatlast=0:eof_action=pass[v]'
        run(['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-i',str(source),'-framerate','30','-i',str(tmp/'frame_%04d.png'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-frames:v',str(frames),'-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',str(out)])
    w2,h2,f2,d2=inspect(out)
    if (w,h,frames)!=(w2,h2,f2) or abs(d2-dur)>.05:raise AssertionError('geometry/frame regression')
    if audio_hash(source)!=audio_hash(out):raise AssertionError('audio regression')
    run(['ffmpeg','-v','error','-xerror','-i',str(out),'-map','0:v:0','-f','null','-','-map','0:a:0','-f','null','-'])
    result={'policy':POLICY,'source_sha256':sha(source),'output_sha256':sha(out),'duration':d2,'frames':f2,'resolution':[w2,h2],'changed_frames':[start,end-1],'month_labels':m['period']['month_labels'],'before_claim':m['period']['claimed_month_count'],'after_claim':m['period']['corrected_month_count'],'audio_adts_unchanged':True,'full_av_decode':'PASS','subtitle_track_count':0,'independent_japanese_asr':'NOT_VERIFIED','rights':'NOT_VERIFIED','mobile_playback':'NOT_VERIFIED'}
    qa.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();[ap.add_argument('--'+a,required=True) for a in ('source','output','manifest','report')];a=ap.parse_args();print(json.dumps(render(a.source,a.output,a.manifest,a.report),ensure_ascii=False))
