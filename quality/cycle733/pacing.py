#!/usr/bin/env python3
"""cycle733: audio-validated, frame-accurate pacing for 10-genre portrait videos.

Removes only scene-tail dead air. Keeps existing images, Japanese voice and burned-in
subtitles in lockstep. Does not call paid services or upload any media.
"""
from __future__ import annotations
import argparse,hashlib,json,math,subprocess
from pathlib import Path
import numpy as np

FPS=30
W,H=1080,1920
SCENES=[(0,78),(78,163),(163,245),(245,331),(331,392),(392,461),(461,531),(531,605)]
DEFAULT_TRIM_FRAMES=15

def run(cmd, binary=False):
    p=subprocess.run(cmd,capture_output=True,check=False,text=not binary)
    if p.returncode:
        err=p.stderr.decode(errors='replace') if binary else p.stderr
        raise RuntimeError(f'command failed {p.returncode}: {err[-1200:]}')
    return p.stdout

def decode_audio(path):
    return np.frombuffer(run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','48000','-f','f32le','-'],True),dtype=np.float32)

def rms_db(a):
    if len(a)==0:return -math.inf
    return 20*math.log10(float(np.sqrt(np.mean(a.astype(np.float64)**2)))+1e-12)

def plan(audio, scenes=SCENES, fps=FPS, trim_frames=DEFAULT_TRIM_FRAMES, rms_limit_db=-35.0):
    if not scenes or scenes[0][0]!=0 or any(b<=a for a,b in scenes):raise ValueError('invalid scene boundaries')
    if any(scenes[i][1]!=scenes[i+1][0] for i in range(len(scenes)-1)):raise ValueError('non-contiguous scenes')
    out=[]
    for i,(start,end) in enumerate(scenes):
        cut=0 if i==len(scenes)-1 else trim_frames
        if cut and end-start<=cut+10:raise ValueError('scene too short')
        tail=audio[int((end-cut)/fps*48000):int(end/fps*48000)] if cut else audio[0:0]
        db=rms_db(tail)
        if cut and db>rms_limit_db:raise ValueError(f'scene {i+1} tail not silent ({db:.1f} dBFS)')
        out.append({'scene':i+1,'source_start_frame':start,'source_end_frame':end,
                    'keep_start_frame':start,'keep_end_frame':end-cut,'trim_frames':cut,
                    'tail_rms_dbfs':round(db,2) if cut else None})
    return out

def make_filter(plans, sample_rate=48000, fps=FPS):
    expr='+'.join(f'between(n,{p["keep_start_frame"]},{p["keep_end_frame"]-1})' for p in plans)
    audio_split=''.join(f'[a{i}]' for i in range(len(plans)))
    parts=[f"[0:v]select='{expr}',setpts=N/({fps}*TB)[v]",
           f'[0:a]asplit={len(plans)}{audio_split}']
    for i,p in enumerate(plans):
        s=round(p['keep_start_frame']/fps*sample_rate)
        e=round(p['keep_end_frame']/fps*sample_rate)
        parts.append(f'[a{i}]atrim=start_sample={s}:end_sample={e},asetpts=PTS-STARTPTS[b{i}]')
    parts.append(''.join(f'[b{i}]' for i in range(len(plans)))+f'concat=n={len(plans)}:v=0:a=1[a]')
    return ';'.join(parts)

def build(source, output):
    source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    audio=decode_audio(source)
    plans=plan(audio)
    flt=make_filter(plans)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-filter_complex',flt,'-map','[v]','-map','[a]','-r',str(FPS),
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',str(output)])
    result={'cycle':733,'previous_cycle':732,'change':'Audio-validated scene-tail dead-air trimming across all 8 scenes',
            'scene_plan':plans,'expected_frames':sum(p['keep_end_frame']-p['keep_start_frame'] for p in plans),
            'original_frames':SCENES[-1][1], 'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'cost_yen':0,'rights':'inherited_media_and_voice_unverified','approval':'HUMAN_REVIEW_NOT_APPROVED',
            'source':str(source),'output':str(output)}
    (output.parent/'build.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True)
    args=ap.parse_args();print(json.dumps(build(args.input,args.output),ensure_ascii=False))
