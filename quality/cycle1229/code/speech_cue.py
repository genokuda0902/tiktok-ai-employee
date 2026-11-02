#!/usr/bin/env python3
"""Offline, genre-neutral voice-aware subtitle underline.

Only a thin rail under the existing burned-in Japanese narration card is edited.
Speech activity is estimated from PCM energy, NOT Japanese ASR. The AAC stream is
copied bit-for-bit and chapter metadata is retained. No network or paid APIs.
"""
import argparse
import array
import hashlib
import json
import math
import subprocess
import tempfile
import wave
from pathlib import Path

GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
PALETTE = {'ai':(78,232,213),'business':(100,181,246),'money':(255,199,97),
           'learning':(157,215,113),'health':(101,221,176),'food':(255,166,122),
           'travel':(126,198,255),'beauty':(255,154,204),'career':(171,162,255),
           'life':(132,224,205)}
W,H,FPS=1080,1920,30
RAIL_X,RAIL_Y,RAIL_W,RAIL_H=112,1377,480,10

def cmd(args, binary=False):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(f'{args[0]} exit {p.returncode}: {p.stderr[-1200:].decode(errors="replace")}')
    return p.stdout if binary else p.stdout.decode()

def probe(path):
    return json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)]))

def aac_sha(path):
    return hashlib.sha256(cmd(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],True)).hexdigest()

def activity_from_pcm(samples,sr,frames,fps=FPS,threshold=.015,hold=3):
    """Per-frame RMS with 3-frame hangover; energy is not a transcript."""
    if sr<=0 or frames<=0 or fps<=0 or threshold<=0 or hold<0:
        raise ValueError('invalid activity parameters')
    energies=[]
    for f in range(frames):
        a=round(f*sr/fps);b=min(len(samples),round((f+1)*sr/fps))
        if a>=b: energies.append(0.0);continue
        energies.append(math.sqrt(sum(int(v)*int(v) for v in samples[a:b])/(b-a))/32768)
    raw=[v>=threshold for v in energies]
    clean=[raw[i] and any(raw[max(0,i-1):min(frames,i+2)]) for i in range(frames)]
    active=[];left=0
    for v in clean:
        if v:left=hold+1
        else:left=max(0,left-1)
        active.append(left>0)
    return active,energies

def chapter_index(t,chapters):
    for i,c in enumerate(chapters):
        if float(c['start_time'])<=t<float(c['end_time']):return i
    return max(0,len(chapters)-1)

def frame_rgba(progress,active,genre,width=RAIL_W,height=RAIL_H):
    if genre not in PALETTE:raise ValueError('unsupported genre')
    if not 0<=progress<=1:raise ValueError('progress must be 0..1')
    if width<8 or height<8:raise ValueError('rail too small')
    out=bytearray(width*height*4)
    fill=min(width,max(0,round(width*progress)))
    rgb=PALETTE[genre]
    for x in range(width):
        for y in range(3,8):
            i=(y*width+x)*4
            if x<fill:
                out[i:i+4]=bytes((*rgb,240)) if active else bytes((44,102,104,200))
            else:
                out[i:i+4]=bytes((12,39,48,210))
    if fill and active:
        for x in range(max(0,fill-3),min(width,fill+2)):
            for y in (2,8):
                i=(y*width+x)*4;out[i:i+4]=bytes((*rgb,160))
    return bytes(out)

def generate_overlay(raw_path,active,chapters,genre):
    frames=len(active)
    with open(raw_path,'wb') as f:
        for i,on in enumerate(active):
            t=(i+.5)/FPS
            c=chapters[chapter_index(t,chapters)]
            a=float(c['start_time']);b=float(c['end_time'])
            progress=max(0.,min(1.,(t-a)/max(.001,b-a)))
            f.write(frame_rgba(progress,on,genre))
    if Path(raw_path).stat().st_size!=frames*RAIL_W*RAIL_H*4:
        raise RuntimeError('overlay frame count mismatch')

def render(source,output,genre='ai',report=None):
    if genre not in GENRES:raise ValueError('unsupported genre')
    source,output=Path(source),Path(output)
    if not source.is_file() or source.resolve()==output.resolve():raise ValueError('invalid paths')
    before=probe(source)
    v=next(s for s in before['streams'] if s['codec_type']=='video')
    a=next(s for s in before['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',W,H,'30/1','aac'):
        raise ValueError('requires H.264 1080x1920 30fps AAC')
    frames=int(v.get('nb_frames',0))
    if frames<30:raise ValueError('source too short')
    duration=frames/FPS
    chapters=before.get('chapters') or [{'start_time':'0','end_time':str(duration),'tags':{'title':'full'}}]
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        wav=Path(td)/'speech.wav';raw=Path(td)/'rail.rgba'
        cmd(['ffmpeg','-v','error','-y','-i',str(source),'-map','0:a:0','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)])
        with wave.open(str(wav),'rb') as wf:
            if wf.getnchannels()!=1 or wf.getsampwidth()!=2:raise ValueError('expected mono 16-bit PCM')
            sr=wf.getframerate();pcm=array.array('h');pcm.frombytes(wf.readframes(wf.getnframes()))
        active,energies=activity_from_pcm(pcm,sr,frames)
        generate_overlay(raw,active,chapters,genre)
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-f','rawvideo','-pixel_format','rgba','-video_size',f'{RAIL_W}x{RAIL_H}',
             '-framerate',str(FPS),'-i',str(raw),
             '-filter_complex',f'[0:v][1:v]overlay={RAIL_X}:{RAIL_Y}:shortest=0:eof_action=repeat:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-map_chapters','0',
             '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
             '-frames:v',str(frames),'-c:a','copy','-metadata:s:a:0','language=jpn',
             '-movflags','+faststart',str(output)])
    after=probe(output)
    ov=next(s for s in after['streams'] if s['codec_type']=='video')
    if (ov['width'],ov['height'],int(ov['nb_frames']))!=(W,H,frames):raise RuntimeError('geometry/frame mismatch')
    if len(after['chapters'])!=len(before.get('chapters',[])):raise RuntimeError('chapter count changed')
    old_aac,new_aac=aac_sha(source),aac_sha(output)
    if old_aac!=new_aac:raise RuntimeError('AAC bitstream changed')
    cmd(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    by_chapter=[]
    for c in chapters:
        start=max(0,round(float(c['start_time'])*FPS));end=min(frames,round(float(c['end_time'])*FPS))
        on=sum(active[start:end]);n=max(1,end-start)
        by_chapter.append({'title':c.get('tags',{}).get('title',''), 'speech_activity_fraction':round(on/n,3),
                           'active_frames':on,'total_frames':end-start})
    qa={'cycle':1229,'previous_cycle':1227,'change':'audio-activity-aware narration underline and chapter speech audit',
        'genre':genre,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'bytes':output.stat().st_size,'resolution':[W,H],'fps':FPS,'frames':frames,
        'duration_s':float(after['format']['duration']),'chapters':len(after['chapters']),
        'speech_threshold_rms':.015,'speech_active_frames':sum(active),
        'speech_activity_fraction':round(sum(active)/frames,3),
        'chapter_speech_audit':by_chapter,'aac_bitstream_identical':True,
        'aac_adts_sha256':new_aac,'full_audio_video_decode':'PASS',
        'independent_japanese_asr':'NOT VERIFIED','subtitle_meaning_timing':'NOT VERIFIED',
        'rights':'NOT VERIFIED','smartphone_real_device':'NOT VERIFIED',
        'reference_v33_direct_comparison':'NOT VERIFIED','publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    if report:Path(report).write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai');p.add_argument('--report')
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,args.report),ensure_ascii=False))
