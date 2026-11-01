#!/usr/bin/env python3
"""Review-only Japanese audio metadata and per-cue signal audit; not ASR."""
from __future__ import annotations
import argparse, hashlib, json, math, re, subprocess
from pathlib import Path
import numpy as np

GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'

def run(args,binary=False):
    p=subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.stdout if binary else p.stdout.decode('utf-8')

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def elementary_hash(path,kind):
    opts=['-map','0:v:0','-c','copy','-f','h264','-'] if kind=='video' else ['-map','0:a:0','-c','copy','-f','adts','-']
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path)]+opts,True)).hexdigest()

def stamp(s):
    m=re.fullmatch(r'(\d\d):(\d\d):(\d\d),(\d\d\d)',s.strip())
    if not m:raise ValueError('invalid SRT time')
    h,minute,sec,milli=map(int,m.groups())
    if minute>59 or sec>59:raise ValueError('invalid SRT range')
    return h*3600+minute*60+sec+milli/1000

def cues_from_srt(path):
    cues=[]
    for block in re.split(r'\n\s*\n',Path(path).read_text(encoding='utf-8-sig').strip()):
        lines=block.splitlines()
        if len(lines)<3 or not lines[0].strip().isdigit():raise ValueError('invalid SRT block')
        m=re.fullmatch(r'(\d\d:\d\d:\d\d,\d\d\d)\s+-->\s+(\d\d:\d\d:\d\d,\d\d\d)',lines[1].strip())
        if not m:raise ValueError('invalid SRT cue')
        start,end=map(stamp,m.groups())
        if end<=start or not ''.join(lines[2:]).strip():raise ValueError('empty/reversed SRT')
        cues.append({'start':start,'end':end,'text':' '.join(lines[2:])})
    if not cues:raise ValueError('no SRT cues')
    for x,y in zip(cues,cues[1:]):
        if y['start']<x['end']-.002:raise ValueError('overlapping SRT')
    return cues

def validate(data,genre,expected=(1080,1920),fps=30):
    if genre not in GENRES:raise ValueError('unknown genre')
    v=[s for s in data['streams'] if s['codec_type']=='video']
    a=[s for s in data['streams'] if s['codec_type']=='audio']
    subs=[s for s in data['streams'] if s['codec_type']=='subtitle']
    if len(v)!=1 or len(a)!=1 or subs:raise ValueError('one video/audio, no soft subtitles required')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac':raise ValueError('H264/AAC required')
    if (v[0]['width'],v[0]['height'])!=expected:raise ValueError('dimensions')
    n,d=map(int,v[0]['avg_frame_rate'].split('/'))
    if not d or abs(n/d-fps)>.01:raise ValueError('fps')
    if int(a[0]['sample_rate'])!=48000:raise ValueError('sample rate')
    duration=float(data['format']['duration'])
    return duration,int(v[0].get('nb_frames') or round(duration*fps))

def signal_audit(source,cues):
    rate=16000
    pcm=run(['ffmpeg','-v','error','-i',str(source),'-map','0:a:0','-ac','1','-ar',str(rate),'-f','s16le','-'],True)
    samples=np.frombuffer(pcm,dtype='<i2').astype(np.float32)/32768.
    window=320
    pad=(-len(samples))%window
    if pad:samples=np.pad(samples,(0,pad))
    rms=np.sqrt(np.mean(samples.reshape(-1,window)**2,axis=1)+1e-12)
    threshold=max(.0025,float(np.percentile(rms,10))*2,float(np.percentile(rms,90))*.08)
    rows=[]
    for i,c in enumerate(cues,1):
        active=rms[max(0,int(c['start']/.02)):min(len(rms),math.ceil(c['end']/.02))]>threshold
        if not len(active):raise ValueError('SRT beyond audio')
        rows.append({'cue':i,'start':c['start'],'end':c['end'],
                     'characters':len(c['text'].replace(' ','')),
                     'chars_per_second':round(len(c['text'].replace(' ',''))/(c['end']-c['start']),2),
                     'signal_active_fraction':round(float(np.mean(active)),3),
                     'signal_present':bool(np.any(active))})
    return {'method':'20ms RMS signal only; NOT independent Japanese ASR','threshold_rms':round(threshold,6),'cues':rows}

def export(source,target,srt,report,manifest,genre='ai',expected=(1080,1920),fps=30):
    source,target,srt,report,manifest=map(lambda p:Path(p).resolve(),(source,target,srt,report,manifest))
    if len({source,target,srt,report,manifest})!=5:raise ValueError('distinct paths required')
    if target.exists() or report.exists():raise FileExistsError('no overwrite')
    if not all(p.is_file() for p in (source,srt,manifest)):raise FileNotFoundError('local inputs missing')
    expected_manifest={'policy':POLICY,'source_sha256':sha(source),'genre':genre,'asset_approval':'review_only_no_public_rights_claim'}
    if json.loads(manifest.read_text())!=expected_manifest:raise ValueError('source hash/policy mismatch')
    duration,frames=validate(probe(source),genre,expected,fps)
    cues=cues_from_srt(srt)
    if cues[-1]['end']>duration+.03:raise ValueError('SRT longer than video')
    audit=signal_audit(source,cues)
    target.parent.mkdir(parents=True,exist_ok=True)
    try:
        run(['ffmpeg','-v','error','-nostdin','-n','-i',str(source),'-map','0:v:0','-map','0:a:0',
             '-c','copy','-metadata:s:a:0','language=jpn',
             '-metadata:s:a:0','handler_name=Japanese narration - review only',
             '-movflags','+faststart',str(target)])
        out=probe(target)
        duration2,frames2=validate(out,genre,expected,fps)
        audio=next(s for s in out['streams'] if s['codec_type']=='audio')
        if audio.get('tags',{}).get('language')!='jpn':raise AssertionError('missing jpn tag')
        if abs(duration2-duration)>.05 or frames2!=frames:raise AssertionError('timeline changed')
        for kind in ('video','audio'):
            if elementary_hash(source,kind)!=elementary_hash(target,kind):raise AssertionError(kind+' changed')
        run(['ffmpeg','-v','error','-xerror','-i',str(target),'-map','0:v:0','-map','0:a:0','-f','null','-'])
        result={'policy':POLICY,'genre':genre,'source_sha256':sha(source),'output_sha256':sha(target),
                'duration':duration2,'frames':frames2,'dimensions':list(expected),'fps':fps,
                'audio_language':'jpn','video_elementary_unchanged':True,'audio_elementary_unchanged':True,
                'full_decode':'PASS','subtitle_tracks':0,'speech_caption_timing_audit':audit,
                'semantic_japanese_asr':'NOT_VERIFIED','publication_approved':False}
        report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        return result
    except BaseException:
        target.unlink(missing_ok=True)
        raise

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('source','output','srt','report','manifest'):p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--genre',choices=GENRES,default='ai')
    a=p.parse_args()
    print(json.dumps(export(a.source,a.output,a.srt,a.report,a.manifest,a.genre),ensure_ascii=False))
