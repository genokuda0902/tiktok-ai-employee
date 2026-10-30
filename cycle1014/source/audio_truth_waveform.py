#!/usr/bin/env python3
"""Review-only soundtrack-derived waveform, NOT ASR or speech verification.

Does not post, upload or approve. Exact private source SHA is mandatory.
The optional synthetic-CI bypass only accepts a <=3s fixture named synthetic_input.mp4.
"""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA = 'fc9abeb4f63929485e1b4cbe5252f3109869ac049c3c77bc86a572b07b65b523'
GENRES = ('ai_work','business','money','learning','health','life','travel','food','tech','history')
FPS = 30
SAMPLE_RATE = 48000
WAVE_X, WAVE_Y = 70, 1710
WAVE_W, WAVE_H = 940, 136


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def run(args, binary=False):
    p=subprocess.run([str(x) for x in args],capture_output=True)
    if p.returncode:
        raise RuntimeError('command failed: '+ ' '.join(map(str,args))+'\n'+p.stderr.decode(errors='replace')[-1600:])
    return p.stdout if binary else p.stdout.decode()


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))


def validate(source,output,genre,review_only,synthetic_ci=False):
    source,output=Path(source).resolve(),Path(output).resolve()
    if genre not in GENRES or not review_only or not source.is_file() or output.exists() or source==output:
        raise ValueError('review-only source/output/genre gate failed')
    info=probe(source); streams=info['streams']
    if len(streams)!=2 or [s['codec_type'] for s in streams]!=['video','audio']:
        raise ValueError('exactly H264 video and AAC audio required')
    v,a=streams
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
        raise ValueError('portrait 1080x1920 30fps H264 required')
    if (a['codec_name'],a['sample_rate'],a.get('tags',{}).get('language'))!=('aac','48000','jpn'):
        raise ValueError('Japanese-tagged AAC 48kHz required')
    if synthetic_ci:
        if source.name!='synthetic_input.mp4' or float(info['format']['duration'])>3.1:
            raise ValueError('synthetic-CI bypass only accepts <=3.1s fixture')
    elif genre!='ai_work' or sha256(source)!=SOURCE_SHA:
        raise ValueError('private source SHA / approved local genre mismatch')
    return int(v['nb_frames'])


def audio_db_frames(source,frames):
    pcm=run(['ffmpeg','-v','error','-i',source,'-vn','-ac','1','-ar',str(SAMPLE_RATE),'-f','f32le','-'],True)
    samples=array('f');samples.frombytes(pcm)
    hop=SAMPLE_RATE//FPS
    levels=[]
    for i in range(frames):
        chunk=samples[i*hop:(i+1)*hop]
        rms=math.sqrt(sum(x*x for x in chunk)/len(chunk)) if chunk else 0
        levels.append(20*math.log10(max(rms,1e-8)))
    return levels


def bar_height(db):
    return max(3,min(58,round(3+55*(db+50)/43)))


def draw_wave(path,levels,frame,frames):
    im=Image.new('RGBA',(WAVE_W,WAVE_H),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,WAVE_W-1,WAVE_H-1),radius=17,fill=(2,14,24,255),outline=(34,93,113,255),width=2)
    d.text((22,8),'AUDIO  /  REAL SIGNAL',fill=(157,231,218,255))
    for i in range(48):
        idx=frame-47+i
        height=bar_height(levels[idx]) if 0<=idx<len(levels) else 3
        x=24+i*18
        d.rounded_rectangle((x,103-height,x+10,103),radius=4,fill=(70,221,190,255) if i<47 else (231,252,246,255))
    d.rounded_rectangle((23,119,917,124),radius=2,fill=(37,70,86,255))
    progress=round(894*(frame+1)/frames)
    if progress>0:d.rounded_rectangle((23,119,23+progress,124),radius=2,fill=(102,237,212,255))
    im.save(path)


def parse_srt(text):
    import re
    cues=[]
    for match in re.finditer(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})',text):
        def sec(t):
            h,m,s=t.replace(',','.').split(':');return int(h)*3600+int(m)*60+float(s)
        cues.append((sec(match.group(1)),sec(match.group(2))))
    return cues


def cue_activity(levels,cues,threshold=-35):
    out=[]
    for start,end in cues:
        lo=max(0,math.floor(start*FPS));hi=min(len(levels),math.ceil(end*FPS))
        if hi<=lo:raise ValueError('empty subtitle interval')
        sample=levels[lo:hi]
        out.append({'start':start,'end':end,'audio_signal_fraction':round(sum(x>threshold for x in sample)/len(sample),3)})
    return out


def audio_hash(path):
    with tempfile.TemporaryDirectory() as d:
        dest=Path(d)/'stream.aac'
        run(['ffmpeg','-v','error','-y','-i',path,'-map','0:a:0','-c','copy','-f','adts',dest])
        return sha256(dest)


def render(source,output,srt,report,genre='ai_work',review_only=False,synthetic_ci=False):
    frames=validate(source,output,genre,review_only,synthetic_ci)
    cues=parse_srt(Path(srt).read_text(encoding='utf-8-sig')) if srt else []
    if not synthetic_ci and len(cues)!=8:raise ValueError('expected eight caption intervals')
    levels=audio_db_frames(source,frames)
    activity=cue_activity(levels,cues)
    if any(x['audio_signal_fraction']<0.15 for x in activity):
        raise ValueError('caption interval has insufficient audio signal: human review required')
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        directory=Path(d)
        for frame in range(frames):draw_wave(directory/f'w_{frame:04d}.png',levels,frame,frames)
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
             '-framerate','30','-i',directory/'w_%04d.png',
             '-filter_complex',f'[0:v][1:v]overlay={WAVE_X}:{WAVE_Y}:shortest=1:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-map_metadata','0','-c:v','libx264',
             '-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30',
             '-frames:v',str(frames),'-c:a','copy','-metadata:s:a:0','language=jpn',
             '-movflags','+faststart',output])
    result=probe(output);v,a=result['streams']
    if len(result['streams'])!=2 or v['width']!=1080 or v['height']!=1920 or int(v['nb_frames'])!=frames or a['codec_name']!='aac':
        raise RuntimeError('output video validation failed')
    for stream in ('v','a'):
        run(['ffmpeg','-v','error','-xerror','-i',output,'-map',f'0:{stream}:0','-f','null','-'])
    before=audio_hash(source);after=audio_hash(output)
    if before!=after:raise RuntimeError('AAC stream changed')
    qa={'input_sha256':sha256(source),'output_sha256':sha256(output),'audio_sha256':after,
        'resolution':[1080,1920],'fps':30,'frames':frames,'duration_seconds':float(result['format']['duration']),
        'cue_audio_activity':activity,'audio_analysis':'PCM RMS soundtrack only, NOT speech recognition',
        'subtitle_semantic_sync':'NOT_VERIFIED','burned_caption_unchanged_by_design':'overlay starts at y=1710',
        'video_audio_full_decode':'PASS','publication':'NOT_APPROVED','employee_approval':False,
        'genre':genre,'synthetic_ci':synthetic_ci}
    Path(report).write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--srt');p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work')
    p.add_argument('--review-only',action='store_true');p.add_argument('--synthetic-ci',action='store_true')
    a=p.parse_args();print(json.dumps(render(a.source,a.output,a.srt,a.report,a.genre,a.review_only,a.synthetic_ci),ensure_ascii=False))
if __name__=='__main__':main()
