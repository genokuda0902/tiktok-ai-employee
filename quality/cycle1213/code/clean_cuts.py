#!/usr/bin/env python3
"""Review-only: replace ghosted slide-transition title/illustration frames.

Generic for ten genres; never edits original narration/subtitle/footer (y>=1140).
No network, paid services, merges or posting.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
WIDTH,HEIGHT,FPS=1080,1920,30
PROTECT_FROM_Y=1140
GENRES=('ai','business','money','learning','health','food','travel','beauty','career','life')
DEFAULT_BOUNDARIES=(42,96,171,252,333,414,501,579)

def validate(boundaries,count,radius=5,lookahead=8,genre='ai'):
    if genre not in GENRES:raise ValueError('Unknown genre')
    if count<=0 or not 1<=radius<lookahead:raise ValueError('Invalid frame count or radius')
    if not boundaries or any(not isinstance(b,int) for b in boundaries):raise ValueError('Integer boundaries required')
    if list(boundaries)!=sorted(set(boundaries)):raise ValueError('Boundaries must be sorted and unique')
    if boundaries[0]-lookahead<0 or boundaries[-1]+lookahead>=count:raise ValueError('Reference out of range')
    if any(b-a<=2*lookahead for a,b in zip(boundaries,boundaries[1:])):raise ValueError('Transitions too close')
    return True

def replacement_map(boundaries,count,radius=5,lookahead=8,genre='ai'):
    validate(boundaries,count,radius,lookahead,genre)
    mapping={}
    for b in boundaries:
        mapping.update({i:b-lookahead for i in range(b-radius,b)})
        mapping.update({i:b+lookahead for i in range(b,b+radius+1)})
    return mapping

def apply_clean_cut(frame,clean_frame,protect_from_y=PROTECT_FROM_Y):
    if frame.shape!=clean_frame.shape or not 0<protect_from_y<frame.shape[0]:
        raise ValueError('Invalid frame shape/protected boundary')
    frame[:protect_from_y]=clean_frame[:protect_from_y]
    return frame

def probe(path):
    j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(s for s in j['streams'] if s['codec_type']=='video')
    a=next(s for s in j['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],int(v['width']),int(v['height']),v['r_frame_rate'])!=('h264',WIDTH,HEIGHT,'30/1'):
        raise ValueError('Require 1080x1920 H264 30fps')
    if a['codec_name']!='aac' or int(a['sample_rate'])!=48000:raise ValueError('Require AAC 48kHz')
    return j

def render(src,dst,boundaries=DEFAULT_BOUNDARIES,radius=5,lookahead=8,genre='ai'):
    src,dst=Path(src),Path(dst)
    probe(src)
    cap=cv2.VideoCapture(str(src))
    if not cap.isOpened():raise RuntimeError('Cannot open source')
    refs={b+d for b in boundaries for d in (-lookahead,lookahead)}
    clean={};count=0
    while True:
        ok,frame=cap.read()
        if not ok:break
        if count in refs:clean[count]=frame.copy()
        count+=1
    cap.release()
    if len(clean)!=len(refs):raise RuntimeError('Missing reference frames')
    mapping=replacement_map(boundaries,count,radius,lookahead,genre)
    cap=cv2.VideoCapture(str(src))
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(src),
         '-map','0:v:0','-map','1:a:0','-map_metadata','1','-map_chapters','1',
         '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(dst)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    n=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if n in mapping:frame=apply_clean_cut(frame,clean[mapping[n]])
            proc.stdin.write(frame.tobytes())
            n+=1
        proc.stdin.close()
        err=proc.stderr.read().decode(errors='replace')
        if proc.wait():raise RuntimeError('FFmpeg: '+err[-1000:])
    except Exception:
        if proc.poll() is None:proc.kill()
        raise
    finally:cap.release()
    if n!=count:raise RuntimeError('Decoded count mismatch')
    v=next(s for s in probe(dst)['streams'] if s['codec_type']=='video')
    if int(v.get('nb_frames',-1))!=count:raise RuntimeError('Encoded frame count mismatch')
    return {'frames':count,'replaced_frames':len(mapping),'genre':genre,
            'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai')
    p.add_argument('--boundaries',default=','.join(map(str,DEFAULT_BOUNDARIES)))
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,tuple(map(int,a.boundaries.split(','))),genre=a.genre),indent=2))
