#!/usr/bin/env python3
"""Local technical QA for 23s review video; not Japanese speech recognition."""
import argparse, json, re, subprocess, cv2, numpy as np
from pathlib import Path

def srt_cues(path):
    s=Path(path).read_text(encoding='utf-8-sig').strip()
    out=[]
    for block in re.split(r'\n\s*\n',s):
        lines=block.splitlines();ts=lines[1].split(' --> ')
        def sec(t):
            h,m,rest=t.split(':');return int(h)*3600+int(m)*60+float(rest.replace(',','.'))
        out.append((sec(ts[0]),sec(ts[1]),' '.join(lines[2:])))
    if len(out)!=8 or any(e<=b for b,e,_ in out) or any(out[i][1]>out[i+1][0]+.001 for i in range(7)):
        raise ValueError('bad Japanese SRT cue timing')
    if abs(out[-1][1]-23.033)>.01:raise ValueError('SRT end mismatch')
    return out

def frames(path):
    c=cv2.VideoCapture(str(path))
    while True:
        ok,x=c.read()
        if not ok:break
        yield cv2.resize(x,(270,480),interpolation=cv2.INTER_AREA)
    c.release()

def verify(src,dst,srt):
    caps=srt_cues(srt)
    teaser=[];outside=[];sub=[];n=0
    for n,(a,b) in enumerate(zip(frames(src),frames(dst)),1):
        d=np.abs(a.astype(np.int16)-b.astype(np.int16))
        i=n-1
        sub.append(float(d[320:465].mean()))
        if 45<=i<87:teaser.append(float(d[:320].mean()))
        else:outside.append(float(d[:320].mean()))
    if n!=691:raise ValueError(f'expected 691 frames, got {n}')
    if min(teaser)<12:raise ValueError('teaser not visually distinct enough')
    if max(outside)>4:raise ValueError('unexpected visual changes outside teaser')
    if max(sub)>4:raise ValueError('protected caption region modified')
    pcm=subprocess.run(['ffmpeg','-v','error','-i',str(dst),'-map','0:a:0','-ac','1',
                        '-ar','16000','-f','f32le','-'],capture_output=True,check=True).stdout
    a=np.frombuffer(pcm,dtype='<f4')
    audio=[]
    for start,end,text in caps:
        chunk=a[int(start*16000):int(end*16000)]
        rms=float(np.sqrt(np.mean(chunk.astype(np.float64)**2)+1e-15))
        audio.append({'start':start,'end':end,'rms_dbfs':round(20*np.log10(max(rms,1e-12)),2),
                      'text':text})
    if any(x['rms_dbfs'] < -45 for x in audio):raise ValueError('audio unexpectedly quiet in a cue')
    return {'frames':n,'subtitle_cues':len(caps),'caption_roi_max_mae_255':round(max(sub),4),
            'teaser_upper_mean_mae_255':round(float(np.mean(teaser)),4),
            'outside_teaser_upper_max_mae_255':round(max(outside),4),
            'audio_cues':audio,'caption_timing_mechanical_check':'PASS',
            'independent_japanese_asr':'NOT_VERIFIED',
            'spoken_content_and_caption_semantic_match':'NOT_VERIFIED',
            'smartphone_playback':'NOT_VERIFIED'}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('source','dest','srt','report'):p.add_argument('--'+key,required=True)
    args=p.parse_args();r=verify(args.source,args.dest,args.srt)
    Path(args.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in r.items() if k!='audio_cues'},ensure_ascii=False))
