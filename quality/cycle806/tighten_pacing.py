#!/usr/bin/env python3
"""Cycle806: speech-preserving, scene-aware pacing for review-only videos.

Uses only the previous review MP4 and timing manifest. No network, stock media,
new TTS, posting or publishing. RMS activity is NOT Japanese ASR verification.
"""
from __future__ import annotations
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

FPS=30
RATE=16000
HOP=160
SILENCE_DBFS=-45.0
TAIL_SECONDS=0.22
MAX_TRIM_SECONDS=0.30
MIN_SCENE_SECONDS=2.0
EXPECTED_GENRES=('ai_work','beauty','love_psychology','money_saving',
                 'sales_business','career','health_life','science',
                 'travel_food','product_life')

def cmdrun(args, *, binary=False):
    p=subprocess.run(args,check=True,capture_output=True)
    return p.stdout if binary else p.stdout.decode('utf-8','replace')

def original_frames(seconds):
    result=[];elapsed=0.;last=0
    for duration in seconds:
        elapsed+=duration
        end=round(elapsed*FPS)
        result.append(end-last)
        last=end
    return result

def load_manifest(path):
    m=json.loads(Path(path).read_text(encoding='utf-8'))
    items=m.get('sentences',[])
    if not items or len(items)>30 or m.get('genre') not in EXPECTED_GENRES:
        raise ValueError('unsupported genre or empty/too-long manifest')
    if m.get('voice_engine')!='Open JTalk':
        raise ValueError('narration provenance must be explicitly identified')
    durations=[]
    for i,item in enumerate(items):
        if item.get('scene')!=i+1 or not isinstance(item.get('text'),str):
            raise ValueError('scene numbers/text mismatch')
        if not item['text'].strip():
            raise ValueError('empty Japanese caption')
        duration=float(item['seconds'])
        if not math.isfinite(duration) or duration<MIN_SCENE_SECONDS or duration>8:
            raise ValueError('invalid scene duration')
        durations.append(duration)
    return m,durations

def decode_pcm(source):
    raw=cmdrun(['ffmpeg','-v','error','-i',str(source),'-map','0:a:0',
                '-ac','1','-ar',str(RATE),'-f','s16le','pipe:1'],binary=True)
    pcm=array('h');pcm.frombytes(raw)
    if sys.byteorder!='little':pcm.byteswap()
    return pcm

def last_active_seconds(samples, threshold_dbfs=SILENCE_DBFS):
    """Last active 10-ms RMS block, not a transcription."""
    limit=(32768*10**(threshold_dbfs/20))**2
    last=-1
    for start in range(0,len(samples)-HOP+1,HOP):
        block=samples[start:start+HOP]
        rms_sq=sum(int(x)*int(x) for x in block)/HOP
        if rms_sq>limit:last=start+HOP
    if last<0:raise ValueError('No audible activity in narration scene')
    return last/RATE

def keep_frames(original_seconds, activity_end, original_frame_count):
    if not 0<activity_end<=original_seconds+0.025:
        raise ValueError('invalid audio activity position')
    target=max(original_seconds-MAX_TRIM_SECONDS,activity_end+TAIL_SECONDS)
    target=min(original_seconds,target)
    keep=min(original_frame_count,math.ceil(target*FPS-1e-8))
    if keep/FPS<MIN_SCENE_SECONDS or (keep<original_frame_count and keep/FPS+0.025<activity_end+TAIL_SECONDS):
        raise ValueError('unsafe trim; might cut spoken audio')
    return keep

def analyze(source,manifest):
    m,durations=load_manifest(manifest)
    pcm=decode_pcm(source)
    if len(pcm)/RATE<sum(durations)-0.15:
        raise ValueError('narration shorter than manifest')
    old=original_frames(durations)
    timeline=[];start_sec=0.;start_frame=0
    for i,(seconds,n) in enumerate(zip(durations,old)):
        lo=round(start_sec*RATE)
        hi=min(len(pcm),round((start_sec+seconds)*RATE))
        activity=last_active_seconds(pcm[lo:hi])
        keep=keep_frames(seconds,activity,n)
        timeline.append(dict(scene=i+1,caption=m['sentences'][i]['text'],
            audio_start=round(start_sec,6),source_start_frame=start_frame,
            source_frames=n,output_frames=keep,
            voice_last_active=round(activity,3),
            trimmed_seconds=round((n-keep)/FPS,3)))
        start_sec+=seconds;start_frame+=n
    return m,timeline

def filter_graph(timeline):
    n=len(timeline)
    filt=[f'[0:v]split={n}'+''.join(f'[sv{i}]' for i in range(n)),
          f'[0:a]asplit={n}'+''.join(f'[sa{i}]' for i in range(n))]
    for i,s in enumerate(timeline):
        a=s['source_start_frame'];b=a+s['output_frames']
        start=s['audio_start'];end=start+s['output_frames']/FPS
        filt.append(f'[sv{i}]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v{i}]')
        filt.append(f'[sa{i}]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS[a{i}]')
    filt.append(''.join(f'[v{i}][a{i}]' for i in range(n))+
                f'concat=n={n}:v=1:a=1[v][a]')
    return ';'.join(filt)

def render(source,manifest,output):
    source=Path(source);output=Path(output)
    m,timeline=analyze(source,manifest)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmdrun(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
        '-filter_complex',filter_graph(timeline),'-map','[v]','-map','[a]',
        '-c:v','libx264','-preset','ultrafast','-crf','22','-pix_fmt','yuv420p',
        '-r',str(FPS),'-c:a','aac','-b:a','128k','-ar','48000',
        '-movflags','+faststart',str(output)])
    cmdrun(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(output),'-f','null','-'])
    metadata=json.loads(cmdrun(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_name,width,height,avg_frame_rate,sample_rate,nb_frames',
        '-of','json',str(output)]))
    streams=metadata['streams']
    video=next(x for x in streams if x['codec_name']=='h264')
    audio=next(x for x in streams if x['codec_name']=='aac')
    total=sum(x['output_frames'] for x in timeline)
    duration=float(metadata['format']['duration'])
    if (video['width'],video['height'],video['avg_frame_rate'])!=(1080,1920,'30/1'):
        raise RuntimeError('Invalid output video resolution/fps')
    if audio.get('sample_rate')!='48000':raise RuntimeError('Invalid output audio sample rate')
    if int(video.get('nb_frames',0))!=total:raise RuntimeError('Unexpected frame count')
    if abs(duration-total/FPS)>0.11:raise RuntimeError('AV timeline drift')
    qa={'cycle':806,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
        'genre':m['genre'],'previous_cycle':805,
        'source_duration_manifest':round(sum(float(x['seconds']) for x in m['sentences']),3),
        'output_duration':round(duration,3),'expected_output_frames':total,
        'total_trimmed_seconds':round(sum(x['trimmed_seconds'] for x in timeline),3),
        'speech_check':'RMS voice activity only; no ASR, Japanese pronunciation or human naturalness verification',
        'captions':'inherited source captions unchanged; segment boundaries retimed',
        'source_audio_rights':'NOT VERIFIED','human_approval':False,'auto_post':False,
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'scenes':timeline,'ffprobe':metadata}
    (output.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--timing',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=render(args.source,args.timing,args.output)
    print(json.dumps({k:result[k] for k in ('output_duration','expected_output_frames','total_trimmed_seconds','output_sha256')},ensure_ascii=False))
