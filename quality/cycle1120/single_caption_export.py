#!/usr/bin/env python3
"""Review-only MP4 with one visible subtitle layer.

The source has burned-in Japanese captions AND a mov_text soft track. Some
players default-enable the soft track, doubling captions. Export H264/AAC
bit-identically with NO soft track and keep the NOT-ASR SRT separately.
No private media is ever uploaded to GitHub.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')

def digest(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def command(args:list[str],binary=False):
    p=subprocess.run(args,check=True,capture_output=True,text=not binary)
    return p.stdout

def inspect(path:Path)->dict:
    return json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def avhash(path:Path,which:str,fmt:str)->str:
    out=command(['ffmpeg','-v','error','-i',str(path),'-map',which,'-c','copy','-f',fmt,'-'],binary=True)
    return hashlib.sha256(out).hexdigest()

def check_media(data:dict,expected=(1080,1920),fps=30):
    streams=data['streams']
    v=[s for s in streams if s['codec_type']=='video']
    a=[s for s in streams if s['codec_type']=='audio']
    s=[s for s in streams if s['codec_type']=='subtitle']
    if len(v)!=1 or len(a)!=1 or v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac':raise ValueError('requires exactly one H264/AAC video and audio')
    if (v[0]['width'],v[0]['height'])!=expected:raise ValueError('wrong dimensions')
    n,d=map(int,v[0]['avg_frame_rate'].split('/'))
    if abs(n/d-fps)>0.01:raise ValueError('wrong fps')
    if int(a[0]['sample_rate'])!=48000:raise ValueError('wrong audio sample rate')
    if len(s)>1 or any(t['codec_name']!='mov_text' for t in s):raise ValueError('unexpected subtitle streams')
    return float(data['format']['duration']),int(v[0].get('nb_frames',round(float(data['format']['duration'])*fps))),len(s)

def export(source:Path,target:Path,srt:Path,report:Path,expected_sha:str,genre:str='ai',expected=(1080,1920),fps=30)->dict:
    if genre not in GENRES:raise ValueError('unknown genre')
    source,target,srt,report=[p.resolve() for p in (source,target,srt,report)]
    if len({source,target,srt,report})!=4:raise ValueError('source, output, SRT and report paths must differ')
    if target.exists() or report.exists():raise FileExistsError('refuse to overwrite outputs')
    if not srt.is_file() or not srt.read_text(encoding='utf-8').strip():raise ValueError('SRT sidecar is required')
    if digest(source)!=expected_sha:raise ValueError('source SHA256 mismatch')
    original=inspect(source)
    duration,frames,soft=check_media(original,expected,fps)
    if soft!=1:raise ValueError('source must have exactly one soft subtitle track')
    source_default=next(s.get('disposition',{}).get('default',0) for s in original['streams'] if s['codec_type']=='subtitle')
    target.parent.mkdir(parents=True,exist_ok=True)
    try:
        command(['ffmpeg','-v','error','-nostdin','-i',str(source),'-map','0:v:0','-map','0:a:0','-c','copy','-sn','-movflags','+faststart',str(target)])
        output=inspect(target)
        d2,f2,soft2=check_media(output,expected,fps)
        if soft2!=0 or len(output['streams'])!=2:raise RuntimeError('subtitle removal failed')
        if abs(d2-duration)>0.035 or f2!=frames:raise RuntimeError('duration or frame count changed')
        if avhash(source,'0:v:0','h264')!=avhash(target,'0:v:0','h264'):raise RuntimeError('H264 bitstream changed')
        if avhash(source,'0:a:0','adts')!=avhash(target,'0:a:0','adts'):raise RuntimeError('AAC bitstream changed')
        command(['ffmpeg','-v','error','-i',str(target),'-map','0:v:0','-map','0:a:0','-f','null','-'])
        result={'source_sha256':expected_sha,'output_sha256':digest(target),'sidecar_srt_sha256':digest(srt),'genre':genre,'duration_seconds':d2,'frames':f2,'resolution':list(expected),'fps':fps,'audio_sample_rate':48000,'source_subtitle_default':source_default,'output_soft_subtitle_tracks':0,'burned_in_caption_pixels':'preserved via H264 bitstream identity (not OCR-verified)','H264_stream':'bit-identical','AAC_stream':'bit-identical','full_av_decode':'PASS','spoken_Japanese_ASR':'NOT VERIFIED','caption_semantic_timing':'NOT VERIFIED','phone_playback':'NOT VERIFIED','rights':'NOT VERIFIED','publication':'NOT APPROVED'}
        report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return result
    except Exception:
        target.unlink(missing_ok=True)
        raise

def main():
    p=argparse.ArgumentParser()
    for flag in ('source','out','srt','report'):p.add_argument('--'+flag,type=Path,required=True)
    p.add_argument('--source-sha',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai')
    a=p.parse_args()
    print(json.dumps(export(a.source,a.out,a.srt,a.report,a.source_sha,a.genre),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
