#!/usr/bin/env python3
"""Rights-gated, review-only restoration of a protected CTA/text region.
Requires a time-aligned CLEAN reference video supplied locally.
Reimplementation, not recovered v33 source. No private assets are bundled.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path

GENRES=('ai_productivity','finance','career','business','education',
        'lifestyle','science','travel','health','entertainment')

def run(args):
    p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(map(str,args))}\n{p.stderr[-2500:]}")
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate,nb_frames',
        '-of','json',path]))

def get_stream(meta,kind):
    return next(s for s in meta['streams'] if s['codec_type']==kind)

def validate(cfg):
    if cfg.get('mode')!='review_only' or cfg.get('publication_approved') is not False or cfg.get('rights_reviewed') is not False:
        raise ValueError('Fail closed: rights and publication must remain unapproved')
    if cfg.get('genre') not in GENRES or set(cfg.get('genres',[]))!=set(GENRES):
        raise ValueError('Ten genre presets required')
    w,h=cfg['canvas'];fps=cfg['fps'];duration=cfg['duration_seconds']
    if (w,h)!=(1080,1920) or fps!=30 or not 1<=duration<=60:
        raise ValueError('Unsupported output geometry, frame rate or duration')
    x,y,bw,bh=cfg['restore_region']
    if not all(type(v) is int for v in (x,y,bw,bh)):
        raise ValueError('Region must be integer pixels')
    if x<0 or y<0 or bw<=0 or bh<=0 or x+bw>w or y+bh>h or any(v%2 for v in (x,y,bw,bh)):
        raise ValueError('Out of bounds or chroma-unsafe region')
    px,py,pw,ph=cfg['protected_cta_box']
    if not (x<=px and y<=py and x+bw>=px+pw and y+bh>=py+ph):
        raise ValueError('Restoration must fully cover protected CTA')
    start,end=cfg['start_seconds'],cfg['end_seconds']
    if not 0<=start<end<=duration or end-start<0.25:
        raise ValueError('Invalid temporal interval')
    if not cfg.get('clean_reference_review_only',False):
        raise ValueError('Explicit clean reference confirmation required')
    return True

def media_match(dirty,clean,cfg):
    a,b=probe(dirty),probe(clean)
    va,vb=get_stream(a,'video'),get_stream(b,'video')
    for v in (va,vb):
        if (v['width'],v['height'])!=tuple(cfg['canvas']) or v['avg_frame_rate']!='30/1':
            raise ValueError('Source geometry or frame rate mismatch')
    da,db=float(a['format']['duration']),float(b['format']['duration'])
    if abs(da-db)>0.045 or abs(da-cfg['duration_seconds'])>0.08:
        raise ValueError('Reference timebase mismatch')
    if 'nb_frames' in va and 'nb_frames' in vb and va['nb_frames']!=vb['nb_frames']:
        raise ValueError('Frame count mismatch')
    get_stream(a,'audio')
    return a,b

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def audio_hash(path,decoded=False):
    fmt=['-f','s16le','-acodec','pcm_s16le','-ac','2','-ar','48000'] if decoded else ['-c:a','copy','-f','adts']
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',*fmt,'-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-1000:])
    return hashlib.sha256(p.stdout).hexdigest()

def render(cfg,dirty,clean,output,report):
    validate(cfg)
    dirty,clean,output=map(Path,(dirty,clean,output))
    if not dirty.is_file() or not clean.is_file():raise FileNotFoundError('Both local source videos required')
    if 'REVIEW_ONLY' not in output.name:raise ValueError('Output must be explicitly review-only')
    source,_=media_match(dirty,clean,cfg)
    x,y,w,h=cfg['restore_region'];start,end=cfg['start_seconds'],cfg['end_seconds']
    output.parent.mkdir(parents=True,exist_ok=True)
    silent=output.parent/(output.stem+'.video_only.mp4')
    filt=(f'[1:v]crop={w}:{h}:{x}:{y}[clean];'
          f"[0:v][clean]overlay={x}:{y}:enable='between(t,{start},{end})':shortest=1,format=yuv420p[v]")
    try:
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',dirty,'-i',clean,
             '-filter_complex',filt,'-map','[v]','-an','-c:v','libx264','-preset','veryfast',
             '-crf','18','-pix_fmt','yuv420p','-frames:v',get_stream(source,'video')['nb_frames'],silent])
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',silent,'-i',dirty,
             '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-movflags','+faststart',output])
    finally:
        silent.unlink(missing_ok=True)
    result=probe(output)
    run(['ffmpeg','-v','error','-i',output,'-f','null','-'])
    if get_stream(result,'video')['nb_frames']!=get_stream(source,'video')['nb_frames']:
        raise ValueError('Output frame count changed')
    if abs(float(result['format']['duration'])-float(source['format']['duration']))>.02:
        raise ValueError('Output duration changed')
    hashes={key:{'before':audio_hash(dirty,key=='pcm'),'after':audio_hash(output,key=='pcm')} for key in ('aac','pcm')}
    if any(x['before']!=x['after'] for x in hashes.values()):raise ValueError('Inherited audio changed')
    qa={'cycle':795,'sha256':sha(output),'duration':float(result['format']['duration']),
        'video':get_stream(result,'video'),'audio':get_stream(result,'audio'),
        'audio_sha256':hashes,'restore_region':cfg['restore_region'],
        'start_seconds':start,'end_seconds':end,'full_decode':'PASS',
        'status':'HUMAN_REVIEW','publication_approved':False,'rights_reviewed':False,
        'japanese_speech_semantics_verified':False,'smartphone_playback_verified':False}
    Path(report).parent.mkdir(parents=True,exist_ok=True)
    Path(report).write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('config','dirty','clean','output','report'):p.add_argument('--'+k,required=True)
    a=p.parse_args()
    print(json.dumps(render(json.loads(Path(a.config).read_text(encoding='utf8')),
        a.dirty,a.clean,a.output,a.report),ensure_ascii=False))
