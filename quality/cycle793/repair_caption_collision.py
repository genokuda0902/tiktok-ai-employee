"""Restore caption-obscured bands from a local pre-caption master.
Review-only reimplementation, NOT original v33. Never upload user assets to CI.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
W,H,FPS=1080,1920,30
DURATION=23.843
GENRES=('ai_productivity','finance','career','business','education','lifestyle','science','travel','health','entertainment')

def intersection(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    return max(0,min(ax+aw,bx+bw)-max(ax,bx))*max(0,min(ay+ah,by+bh)-max(ay,by))

def validate(cfg):
    if cfg.get('mode')!='review_only' or cfg.get('rights_reviewed') is not False or cfg.get('publication_approved') is not False:
        raise ValueError('FAIL CLOSED: rights/publication review required')
    if cfg.get('genre') not in GENRES or set(cfg.get('genres',[]))!=set(GENRES):
        raise ValueError('unknown genre or incomplete 10-genre config')
    if cfg.get('canvas')!=[W,H] or cfg.get('fps')!=FPS or abs(cfg.get('duration_seconds',0)-DURATION)>.005:
        raise ValueError('bad video specification')
    rules=cfg.get('collision_rules',[])
    if not rules: raise ValueError('no collision rules')
    for r in rules:
        start,end=r['start'],r['end']
        if not 0<=start<end<=DURATION: raise ValueError('invalid interval')
        for key in ('caption_box','protected_box','repair_band'):
            x,y,w,h=r[key]
            if any(type(v) is not int for v in (x,y,w,h)) or not (0<=x<W and 0<=y<H and w>0 and h>0 and x+w<=W and y+h<=H):
                raise ValueError('invalid rectangle: '+key)
        if intersection(r['caption_box'],r['protected_box'])==0:
            raise ValueError('caption and protected region do not collide')
        if intersection(r['repair_band'],r['caption_box'])!=r['caption_box'][2]*r['caption_box'][3]:
            raise ValueError('repair band must cover entire offending caption')
    return True

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError('command failed: '+' '.join(cmd)+'\n'+p.stderr[-5000:])
    return p.stdout

def probe(path):
    p=json.loads(run(['ffprobe','-v','error','-show_entries',
      'format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate,r_frame_rate,nb_frames',
      '-of','json',str(path)]))
    video=next((s for s in p['streams'] if s['codec_type']=='video'),None)
    audio=next((s for s in p['streams'] if s['codec_type']=='audio'),None)
    if not video or not audio or video.get('width')!=W or video.get('height')!=H:
        raise ValueError('missing audio/video or wrong dimensions')
    if abs(float(p['format']['duration'])-DURATION)>.06: raise ValueError('duration mismatch')
    from fractions import Fraction
    rate=float(Fraction(video['r_frame_rate']))
    count=int(video.get('nb_frames','714'))
    if abs(rate-30)>0.2 or not 710<=count<=716:
        raise ValueError(f'wrong nominal FPS/frame count: {video}')
    return p

def render(cfg,obstructed,clean,output):
    validate(cfg)
    obstructed,clean,output=map(Path,(obstructed,clean,output))
    if not obstructed.is_file() or not clean.is_file():
        raise FileNotFoundError('both local source videos are required')
    if '_REVIEW_ONLY' not in output.name: raise ValueError('review-only label required')
    probe(obstructed); probe(clean)
    chain='[0:v]setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[clean];'
    last='v0'
    for i,r in enumerate(cfg['collision_rules']):
        x,y,w,h=r['repair_band']
        if i==0: chain+=f'[clean]crop={w}:{h}:{x}:{y}[band{i}];'
        else: chain+=f'[1:v]crop={w}:{h}:{x}:{y}[band{i}];'
        chain+=(f'[{last}][band{i}]overlay={x}:{y}:eof_action=pass:'
                f"enable='between(t,{r['start']},{r['end']})'[v{i+1}];")
        last=f'v{i+1}'
    chain+=f'[{last}]fps={FPS},setpts=N/({FPS}*TB)[vout]'
    output.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(obstructed),
         '-i',str(clean),'-filter_complex',chain,'-map','[vout]','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)])
    p=probe(output)
    run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
    return {'cycle':793,'status':'HUMAN_REVIEW','publication_approved':False,
      'rights_reviewed':False,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
      'video':next(s for s in p['streams'] if s['codec_type']=='video'),
      'audio':next(s for s in p['streams'] if s['codec_type']=='audio'),
      'duration_seconds':float(p['format']['duration']),
      'repaired_intervals':[[r['start'],r['end']] for r in cfg['collision_rules']],
      'japanese_speech_transcript_verified':False,'caption_semantics_verified':False,
      'asset_rights_verified':False}

def main():
    p=argparse.ArgumentParser()
    for key in ('config','input','clean','output','report'):p.add_argument('--'+key,required=True)
    a=p.parse_args()
    cfg=json.loads(Path(a.config).read_text(encoding='utf-8'))
    result=render(cfg,a.input,a.clean,a.output)
    Path(a.report).parent.mkdir(parents=True,exist_ok=True)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
