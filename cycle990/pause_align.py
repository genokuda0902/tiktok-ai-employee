#!/usr/bin/env python3
"""Review-only pause-aware Japanese captions. RMS is NOT ASR/semantic sync."""
import argparse
import array
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from cycle988 import caption_mux

WINDOW_SEC=0.070
MAX_SHIFT_SEC=0.280
STEP_SEC=0.020
QUIET_RMS=0.012
MIN_GAIN=0.50

def call(args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout

def audio_pcm(source):
    data=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error',
        '-i',str(source),'-map','0:a:0','-ac','1','-ar','16000',
        '-f','s16le','-'],check=True,capture_output=True).stdout
    samples=array.array('h')
    samples.frombytes(data)
    if sys.byteorder!='little': samples.byteswap()
    if not samples: raise ValueError('Audio is empty')
    return samples,16000

def energy(samples,sr,t):
    left=max(0,int(round((t-WINDOW_SEC)*sr)))
    right=min(len(samples),int(round((t+WINDOW_SEC)*sr)))
    if right<=left: return 1.0
    return math.sqrt(sum(float(v)*v for v in samples[left:right])/(right-left))/32768.0

def optimize(cues,samples,sr,duration):
    """Adjust internal boundaries only when a nearby low-energy interval exists."""
    if len(cues)<2: return [dict(x) for x in cues],[]
    new=[dict(x) for x in cues]
    reports=[]
    for i in range(len(cues)-1):
        old=float(cues[i]['end'])
        baseline=energy(samples,sr,old)
        best=old
        best_rms=baseline
        candidates=[]
        for k in range(-14,15):
            t=round(old+k*STEP_SEC,3)
            if t<=float(cues[i]['start'])+0.6 or t>=float(cues[i+1]['end'])-0.6:
                continue
            e=energy(samples,sr,t)
            if e<=QUIET_RMS and e<=baseline*MIN_GAIN:
                candidates.append((abs(t-old),e,t))
        if candidates:
            _,best_rms,best=min(candidates)
        new[i]['end']=best
        new[i+1]['start']=best
        reports.append({'boundary':i+1,'old_s':round(old,3),'new_s':round(best,3),
            'delta_ms':round((best-old)*1000),'old_rms':round(baseline,6),
            'new_rms':round(best_rms,6),'pause_proxy_only':True})
    caption_mux.validate({'language':'ja','review_only':True,'cues':new},
                         duration,'ai_work',synthetic=True)
    return new,reports

def run(source,output,manifest,work,expected_sha=None,genre='ai_work',synthetic=False):
    source,output,manifest,work=map(Path,(source,output,manifest,work))
    if not source.is_file() or not manifest.is_file():
        raise FileNotFoundError('Missing source or manifest')
    if source.resolve()==output.resolve():
        raise ValueError('Never overwrite input')
    digest=caption_mux.sha256(source)
    if not synthetic and (not expected_sha or expected_sha!=digest):
        raise ValueError('Explicit exact source SHA256 required')
    info=caption_mux.probe(source)
    v=[s for s in info['streams'] if s['codec_type']=='video']
    a=[s for s in info['streams'] if s['codec_type']=='audio']
    subs=[s for s in info['streams'] if s['codec_type']=='subtitle']
    if len(v)!=1 or len(a)!=1 or len(subs)!=1 or subs[0]['codec_name']!='mov_text':
        raise ValueError('Expected H264/AAC + one mov_text track')
    if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'])!=('h264',1080,1920,'30/1'):
        raise ValueError('Unreviewed video properties')
    if a[0]['codec_name']!='aac':
        raise ValueError('Unreviewed audio codec')
    duration=float(info['format']['duration'])
    original=json.loads(manifest.read_text(encoding='utf-8'))
    cues=caption_mux.validate(original,duration,genre,synthetic)
    pcm,sr=audio_pcm(source)
    aligned,changes=optimize(cues,pcm,sr,duration)
    work.mkdir(parents=True,exist_ok=True)
    output.parent.mkdir(parents=True,exist_ok=True)
    clean=work/'no_subtitle.mp4'
    call(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
        '-map','0:v:0','-map','0:a:0','-c','copy','-movflags','+faststart',str(clean)])
    new_manifest={**original,'cues':aligned,
        'provenance':'Audio RMS pause proxy only; NOT independent Japanese ASR/semantic sync',
        'publication_approved':False}
    mf=work/'aligned_manifest.json'
    mf.write_text(json.dumps(new_manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    mux=caption_mux.render(clean,output,mf,work/'mux',
        expected_sha=caption_mux.sha256(clean),genre=genre,synthetic=synthetic)
    report={'cycle':990,'input_sha256':digest,'output_sha256':mux['output_sha256'],
        'genre':genre,'duration':duration,'cues':len(aligned),
        'boundaries_changed':sum(x['delta_ms']!=0 for x in changes),
        'rms_boundary_audit':changes,'max_shift_ms':int(MAX_SHIFT_SEC*1000),
        'video_audio_stream_copy':True,'independent_asr':False,
        'semantic_caption_alignment_verified':False,'burned_captions_unchanged':True,
        'review_only':True,'publication_approved':False}
    (work/'qa_pause.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for opt in ('source','output','manifest','work'):
        p.add_argument('--'+opt,required=True)
    p.add_argument('--expected-sha')
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--synthetic',action='store_true')
    args=p.parse_args()
    print(json.dumps(run(args.source,args.output,args.manifest,args.work,
        args.expected_sha,args.genre,args.synthetic),ensure_ascii=False,indent=2))
