"""Deterministic, original 7-cut SFX; review-only, no third-party audio.
Copy H264 bitstream unchanged. Preserve chapters and Japanese narration.
Only Python standard library and FFmpeg required.
"""
import argparse, hashlib, json, math, random, struct, subprocess, wave
from pathlib import Path
SAMPLE_RATE=48000
CUE_SECONDS=0.16
PEAK_DBFS=-22.0
MAX_SHIFT_SECONDS=0.18
SEED=1147

def run(cmd,capture=False):
    p=subprocess.run(cmd,check=True,stdout=subprocess.PIPE if capture else None,
                     stderr=subprocess.PIPE if capture else None)
    return p.stdout.decode() if capture else None

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_chapters','-show_streams',
                           '-show_format','-of','json',str(path)],True))

def boundaries_from_chapters(path):
    return sorted(set(float(c['start_time']) for c in probe(path).get('chapters',[])
                      if float(c['start_time'])>0.001))

def mono_pcm(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
                      '-ac','1','-ar',str(SAMPLE_RATE),'-f','s16le','-'],
                     check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return memoryview(p.stdout).cast('h')

def window_rms(pcm,start,length=CUE_SECONDS):
    a=max(0,round(start*SAMPLE_RATE))
    b=min(len(pcm),round((start+length)*SAMPLE_RATE))
    if b<=a:return float('inf')
    s=0;n=0
    for i in range(a,b,8):
        v=pcm[i]/32768.0;s+=v*v;n+=1
    return math.sqrt(s/max(1,n))

def quiet_placements(pcm,boundaries):
    duration=len(pcm)/SAMPLE_RATE
    result=[]
    for boundary in boundaries:
        choices=[]
        for k in range(-9,10):
            offset=k*.02;start=boundary+offset
            if start<0 or start+CUE_SECONDS>duration:continue
            rms=window_rms(pcm,start)
            choices.append((rms+.0008*abs(offset)/MAX_SHIFT_SECONDS,abs(offset),start,rms))
        if not choices:raise ValueError('No valid sound cue window')
        _,_,start,rms=min(choices)
        result.append({'chapter_time':round(boundary,3),'cue_start':round(start,3),
                       'offset_ms':round((start-boundary)*1000),
                       'speech_window_rms_dbfs':round(20*math.log10(max(rms,1e-10)),2)})
    return result

def cue_samples():
    rng=random.Random(SEED);n=round(CUE_SECONDS*SAMPLE_RATE)
    fast=slow=0.0;out=[]
    for i in range(n):
        t=i/SAMPLE_RATE;white=rng.uniform(-1,1)
        fast=.72*fast+.28*white;slow=.978*slow+.022*white
        band=fast-slow
        tone=math.sin(2*math.pi*(630*t+2600*t*t))
        attack=min(1.0,t/.009)
        decay=max(0.0,(CUE_SECONDS-t)/CUE_SECONDS)**1.8
        out.append((.83*band+.17*tone)*attack*decay)
    scale=10**(PEAK_DBFS/20)/max(abs(v) for v in out)
    return [v*scale for v in out]

def write_stem(path,duration,placements):
    n=round(duration*SAMPLE_RATE);buf=[0.0]*n
    samples=cue_samples()
    for p in placements:
        start=round(p['cue_start']*SAMPLE_RATE)
        for i,v in enumerate(samples):
            if start+i<n:buf[start+i]+=v
    peak=max(abs(v) for v in buf)
    if peak>=.99:raise ValueError('Unsafe SFX peak')
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(SAMPLE_RATE)
        for i in range(0,n,16384):
            chunk=buf[i:i+16384]
            f.writeframesraw(struct.pack('<'+'h'*len(chunk),
              *(int(max(-1,min(1,v))*32767) for v in chunk)))
    return peak

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def render(source,output,stem,expected_sha,boundaries=None):
    source=Path(source);output=Path(output);stem=Path(stem)
    if sha256(source)!=expected_sha:raise ValueError('Source checksum mismatch')
    info=probe(source)
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    if v['codec_name']!='h264' or a['codec_name']!='aac':
        raise ValueError('Expected H264/AAC source')
    duration=float(info['format']['duration'])
    boundaries=boundaries if boundaries is not None else boundaries_from_chapters(source)
    if not boundaries:raise ValueError('No chapter boundaries')
    placements=quiet_placements(mono_pcm(source),boundaries)
    stem.parent.mkdir(parents=True,exist_ok=True)
    peak=write_stem(stem,duration,placements)
    output.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(stem),
         '-filter_complex','[0:a:0][1:a:0]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]',
         '-map','0:v:0','-map','[aout]','-map_metadata','0','-map_chapters','0',
         '-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','1',
         '-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)])
    return {'source_sha256':expected_sha,'output_sha256':sha256(output),
            'sfx_stem_sha256':sha256(stem),'sfx_peak_dbfs':round(20*math.log10(peak),2),
            'chapter_boundaries':boundaries,'cue_placements':placements,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output');p.add_argument('stem')
    p.add_argument('source_sha256')
    p.add_argument('--boundaries',help='comma-separated for synthetic CI')
    a=p.parse_args()
    bs=[float(x) for x in a.boundaries.split(',')] if a.boundaries else None
    print(json.dumps(render(a.source,a.output,a.stem,a.source_sha256,bs),indent=2))
