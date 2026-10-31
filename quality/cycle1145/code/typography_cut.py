"""Review-only Japanese title crossfade ghost repair. Never post or merge automatically."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

WIDTH,HEIGHT,FPS=1080,1920,30
TOP_HEIGHT,FEATHER=1170,40
OLD_REFERENCE,NEW_REFERENCE=36,50
OLD_START,OLD_END,NEW_START,NEW_END=38,41,42,49
GENRES=('ai_workflow','business','finance','health','beauty','travel','education','lifestyle','technology','entertainment')

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def alpha_mask(height=TOP_HEIGHT,feather=FEATHER):
    if not (0<feather<height<=HEIGHT): raise ValueError('Invalid protected boundary')
    a=np.full(height,255,dtype=np.uint8)
    a[height-feather:]=np.round(np.linspace(255,0,feather)).astype(np.uint8)
    return a

def clean_plate(frame_bgr):
    if frame_bgr.shape!=(HEIGHT,WIDTH,3): raise ValueError('1080x1920 BGR required')
    plate=cv2.cvtColor(frame_bgr[:TOP_HEIGHT],cv2.COLOR_BGR2RGBA)
    plate[:,:,3]=alpha_mask()[:,None]
    return Image.fromarray(plate,'RGBA')

def source_info(source):
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)],text=True))
    v=next(x for x in d['streams'] if x['codec_type']=='video')
    a=next(x for x in d['streams'] if x['codec_type']=='audio')
    return dict(width=v['width'],height=v['height'],fps=v['avg_frame_rate'],frames=int(v.get('nb_frames',0)),duration=float(d['format']['duration']),video_codec=v['codec_name'],audio_codec=a['codec_name'],sample_rate=int(a['sample_rate']))

def verify_source(info):
    if (info['width'],info['height'],info['fps'])!=(WIDTH,HEIGHT,'30/1'): raise ValueError('1080x1920 30fps required')
    if (info['audio_codec'],info['sample_rate'])!=('aac',48000): raise ValueError('AAC 48kHz required')
    if info['frames'] and info['frames']<=NEW_REFERENCE: raise ValueError('Not enough frames')

def extract_frames(source):
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError('Cannot decode source')
    found={}
    for i in range(NEW_REFERENCE+1):
        ok,f=cap.read()
        if not ok: break
        if i in (OLD_REFERENCE,NEW_REFERENCE): found[i]=f.copy()
    cap.release()
    if len(found)!=2: raise RuntimeError('Missing clean reference frame')
    return found

def graph():
    return (f"[0:v][1:v]overlay=0:0:format=auto:shortest=1:enable='between(n,{OLD_START},{OLD_END})'[tmp];"
            f"[tmp][2:v]overlay=0:0:format=auto:shortest=1:enable='between(n,{NEW_START},{NEW_END})',format=yuv420p[v]")

def render(source,output,expected_sha256,genre='ai_workflow',max_frames=None):
    if genre not in GENRES: raise ValueError('Unknown genre')
    source,output=Path(source),Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    actual=sha256(source)
    if actual!=expected_sha256: raise ValueError('Source SHA-256 mismatch; fail closed')
    verify_source(source_info(source))
    if max_frames is not None and max_frames<=NEW_END: raise ValueError('Too few frames')
    frames=extract_frames(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        old,new=Path(d)/'old.png',Path(d)/'new.png'
        clean_plate(frames[OLD_REFERENCE]).save(old)
        clean_plate(frames[NEW_REFERENCE]).save(new)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-loop','1','-framerate','30','-i',str(old),
             '-loop','1','-framerate','30','-i',str(new),
             '-filter_complex',graph(),'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','19','-threads','4',
             '-pix_fmt','yuv420p','-r','30','-c:a','copy',
             '-map_metadata','0','-map_chapters','0','-movflags','+faststart']
        if max_frames is not None: cmd+=['-frames:v',str(max_frames)]
        subprocess.run(cmd+[str(output)],check=True)
    return {'genre':genre,'source_sha256':actual,'output_sha256':sha256(output),
            'replaced_frames':list(range(OLD_START,NEW_END+1)),
            'protected_caption_region':f'y>={TOP_HEIGHT}',
            'audio':'AAC stream copy',
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--expected-sha256',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai_workflow')
    p.add_argument('--max-frames',type=int)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.expected_sha256,a.genre,a.max_frames),indent=2,ensure_ascii=False))
