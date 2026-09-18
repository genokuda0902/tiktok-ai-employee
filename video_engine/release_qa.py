#!/usr/bin/env python3
"""Evidence-based TikTok MP4 preflight. Human approval is always required."""
import argparse,hashlib,json,math,re,subprocess
from pathlib import Path

def execute(args):
    return subprocess.run(args,capture_output=True,text=True)

def inspect(video,captions=None,report=None):
    path=Path(video).resolve()
    if not path.is_file() or not path.stat().st_size: raise FileNotFoundError(path)
    probe=execute(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    if probe.returncode: raise RuntimeError(probe.stderr)
    data=json.loads(probe.stdout); video_streams=[s for s in data['streams'] if s['codec_type']=='video'];audio_streams=[s for s in data['streams'] if s['codec_type']=='audio']
    if len(video_streams)!=1: raise ValueError('Exactly one video stream required')
    w,h=int(video_streams[0]['width']),int(video_streams[0]['height']);duration=float(data['format']['duration'])
    checks={'portrait_9_16':w*16==h*9,'resolution_1080x1920':(w,h)==(1080,1920),'duration_positive':math.isfinite(duration) and duration>0,'audio_track':bool(audio_streams)}
    v=execute(['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0','-f','null','-']);checks['video_decodes']=v.returncode==0
    mean_db=None
    if audio_streams:
        a=execute(['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:a:0','-f','null','-']);checks['audio_decodes']=a.returncode==0
        loud=execute(['ffmpeg','-hide_banner','-i',str(path),'-map','0:a:0','-af','volumedetect','-f','null','-']);m=re.search(r'mean_volume:\s*(-?[\d.]+) dB',loud.stderr)
        mean_db=float(m.group(1)) if m else None;checks['audio_non_silent']=mean_db is not None and mean_db>-55
    else:checks.update(audio_decodes=False,audio_non_silent=False)
    entries=[]
    if captions:
        for i,c in enumerate(json.loads(Path(captions).read_text(encoding='utf8'))):
            start,end=float(c['start']),float(c['end']);item={'index':i,'time_valid':0<=start<end<=duration+.05,'text_present':bool(str(c.get('text','')).strip())}
            if 'bbox' in c:
                x1,y1,x2,y2=map(float,c['bbox']);item['bbox_in_frame']=0<=x1<x2<=w and 0<=y1<y2<=h;item['safe_zone']=x1>=w*.08 and x2<=w*.92 and y1>=h*.13 and y2<=h*.78
            else:item['bbox_in_frame']=None;item['safe_zone']=None
            entries.append(item)
        checks['caption_metadata_valid']=bool(entries) and all(c['time_valid'] and c['text_present'] and c['bbox_in_frame'] is not False for c in entries)
    else:checks['caption_metadata_valid']=None
    required=[v for k,v in checks.items() if k!='resolution_1080x1920' and v is not None]
    result={'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions':[w,h],'duration_seconds':duration,'audio_mean_db':mean_db,'checks':checks,'captions':entries,'status':'REJECT_TECHNICAL' if not all(required) else 'HUMAN_REVIEW_REQUIRED','human_review_required':['watch full video at phone size','check cropping and embedded text','listen to pronunciation and subtitle timing','verify asset rights/privacy and factual claims'],'decode_error':v.stderr[-1000:]}
    dest=Path(report) if report else path.with_suffix('.qa.json');dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result['status']=='REJECT_TECHNICAL' else 0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--captions');p.add_argument('--report');a=p.parse_args();raise SystemExit(inspect(a.video,a.captions,a.report))
