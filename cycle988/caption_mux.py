#!/usr/bin/env python3
"""Review-only Japanese timed-caption MP4 mux. Never uploads source media."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

GENRES = ('ai_work','finance','learning','health','travel','food','science','history','business','lifestyle')

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1048576),b''):
            h.update(b)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def fmt(t):
    n=round(t*1000)
    h,n=divmod(n,3600000)
    m,n=divmod(n,60000)
    s,n=divmod(n,1000)
    return f'{h:02}:{m:02}:{s:02},{n:03}'

def validate(manifest,duration,genre,synthetic=False):
    if genre not in GENRES:
        raise ValueError('Unknown genre')
    if genre!='ai_work' and not synthetic:
        raise ValueError('Unreviewed genre: fail closed')
    if manifest.get('language')!='ja' or manifest.get('review_only') is not True:
        raise ValueError('Japanese review-only manifest required')
    cues=manifest.get('cues')
    if not isinstance(cues,list) or not 0<len(cues)<=100:
        raise ValueError('Invalid cues')
    previous=0.0
    for c in cues:
        a,b,t=c['start'],c['end'],c['text']
        if not isinstance(a,(int,float)) or not isinstance(b,(int,float)):
            raise ValueError('Invalid cue times')
        if a<previous-0.002 or a>=b or b>duration+0.02:
            raise ValueError('Overlapping/out-of-range cue')
        if not isinstance(t,str) or not t.strip() or len(t)>80 or re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',t):
            raise ValueError('Invalid caption text')
        previous=b
    if abs(cues[0]['start'])>0.001 or abs(cues[-1]['end']-duration)>0.06:
        raise ValueError('Caption coverage does not span video')
    return cues

def make_srt(cues):
    return ''.join(f'{i}\n{fmt(c["start"])} --> {fmt(c["end"])}\n{c["text"]}\n\n' for i,c in enumerate(cues,1))

def atoms(data,start,stop):
    i=start
    while i+8<=stop:
        n=int.from_bytes(data[i:i+4],'big')
        kind=bytes(data[i+4:i+8])
        header=8
        if n==1:
            if i+16>stop:
                raise ValueError('Truncated atom')
            n=int.from_bytes(data[i+8:i+16],'big')
            header=16
        if n==0:
            n=stop-i
        if n<header or i+n>stop:
            raise ValueError('Malformed MP4 atom')
        yield kind,i+header,i+n
        i+=n

def disable_default_subtitle(path):
    # FFmpeg's MP4 muxer auto-enables the first mov_text track even when
    # -disposition:s:0 0 is set. Clear only the subtitle tkhd enabled bit.
    path=Path(path)
    data=bytearray(path.read_bytes())
    count=0
    for kind,a,b in atoms(data,0,len(data)):
        if kind!=b'moov':
            continue
        for kind2,c,d in atoms(data,a,b):
            if kind2!=b'trak':
                continue
            flag=None
            handler=None
            for kind3,e,f in atoms(data,c,d):
                if kind3==b'tkhd':
                    flag=e+3
                if kind3==b'mdia':
                    for kind4,g,h in atoms(data,e,f):
                        if kind4==b'hdlr':
                            handler=bytes(data[g+8:g+12])
            if handler in (b'text',b'sbtl',b'subt'):
                if flag is None:
                    raise ValueError('Missing subtitle tkhd')
                data[flag]&=0xFE
                count+=1
    if count!=1:
        raise ValueError(f'Expected one subtitle track, found {count}')
    path.write_bytes(data)

def render(source,output,manifest_file,work,expected_sha=None,genre='ai_work',synthetic=False):
    source,output,manifest_file,work=map(Path,(source,output,manifest_file,work))
    if not source.is_file() or not manifest_file.is_file():
        raise FileNotFoundError('Source/manifest missing')
    if source.resolve()==output.resolve():
        raise ValueError('Refuse to overwrite source')
    digest=sha256(source)
    if not synthetic and (not expected_sha or digest!=expected_sha):
        raise ValueError('Exact source SHA approval required')
    info=probe(source)
    streams=info['streams']
    v=[s for s in streams if s['codec_type']=='video']
    a=[s for s in streams if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or any(s['codec_type']=='subtitle' for s in streams):
        raise ValueError('Expected one video and one audio, no prior subtitle')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac':
        raise ValueError('Unexpected codecs')
    if (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('Unreviewed resolution or FPS')
    duration=float(info['format']['duration'])
    cues=validate(json.loads(manifest_file.read_text(encoding='utf-8')),duration,genre,synthetic)
    work.mkdir(parents=True,exist_ok=True)
    output.parent.mkdir(parents=True,exist_ok=True)
    srt=work/'captions_ja.srt'
    srt.write_text(make_srt(cues),encoding='utf-8')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-f','srt','-i',str(srt),'-map','0:v:0','-map','0:a:0','-map','1:0',
         '-c:v','copy','-c:a','copy','-c:s','mov_text',
         '-metadata:s:s:0','language=jpn','-disposition:s:0','0',
         '-movflags','+faststart',str(output)])
    disable_default_subtitle(output)
    out=probe(output)
    subs=[s for s in out['streams'] if s['codec_type']=='subtitle']
    if len(subs)!=1 or subs[0]['codec_name']!='mov_text' or subs[0].get('tags',{}).get('language')!='jpn':
        raise RuntimeError('Missing Japanese text track')
    if subs[0].get('disposition',{}).get('default'):
        raise RuntimeError('Subtitle must be OFF by default')
    if abs(float(out['format']['duration'])-duration)>.05:
        raise RuntimeError('Duration changed')
    return {'source_sha256':digest,'output_sha256':sha256(output),'cues':len(cues),
            'duration':duration,'video_audio_stream_copy':True,
            'subtitle_language':'jpn','subtitle_default_off':True,
            'review_only':True,'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for opt in ('source','output','manifest','work'):
        p.add_argument('--'+opt,required=True)
    p.add_argument('--expected-sha')
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--synthetic',action='store_true')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.work,a.expected_sha,a.genre,a.synthetic),
                     ensure_ascii=False,indent=2))
