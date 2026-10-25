"""cycle838: 7 frame-accurate photo-area dissolves across 8 scenes.

Review-only reimplementation. No public assets, service access, auto-posting or
rights approval. Existing audio is copied unchanged; subtitle/CTA region is protected.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from cycle833.focal_layout import GENRES, FRAMES, PHOTO_RECT, CAPTION_RECT

FPS=30
WIDTH,HEIGHT=1080,1920
TRANSITION_FRAMES=8
REQUIRED={
    'data_classification':'fictional',
    'contains_personal_data':False,
    'review_only':True,
    'publication_approved':False,
    'source_rights_reviewed':False,
    'external_upload':False,
    'automatic_posting':False,
}

def validate(genre:str,manifest:dict,transition_frames:int=TRANSITION_FRAMES)->tuple[int,...]:
    if genre not in GENRES or len(GENRES)!=10:
        raise ValueError('Unknown genre or missing ten-genre preset')
    if not isinstance(manifest,dict) or any(manifest.get(k)!=v for k,v in REQUIRED.items()):
        raise ValueError('Fail-closed: fictional local human-review-only provenance required')
    if type(transition_frames) is not int or not 3<=transition_frames<=12:
        raise ValueError('Transition length must be 3..12 frames')
    l,t,r,b=PHOTO_RECT
    if not (0<=l<r<=WIDTH and 0<=t<b<CAPTION_RECT[1]):
        raise ValueError('Photo region must not overlap captions')
    if len(FRAMES)!=8 or any(f<=transition_frames*2 for f in FRAMES):
        raise ValueError('Scene frame plan cannot support transitions')
    return tuple(sum(FRAMES[:i]) for i in range(1,len(FRAMES)))

def overlay_graph(boundaries:tuple[int,...],count:int=TRANSITION_FRAMES)->str:
    segments=[]
    previous='0:v'
    l,t,r,b=PHOTO_RECT
    for i,cut in enumerate(boundaries,start=1):
        duration=count/FPS
        segments.append(
            f'[{i}:v]format=rgba,fade=t=out:st=0:d={duration:.9f}:alpha=1,'
            f'setpts=PTS-STARTPTS+{cut}/({FPS}*TB)[fade{i}]'
        )
        segments.append(
            f'[{previous}][fade{i}]overlay={l}:{t}:'
            f'eof_action=pass:repeatlast=0:format=auto[v{i}]'
        )
        previous=f'v{i}'
    segments.append(f'[{previous}]format=yuv420p[vout]')
    return ';'.join(segments)

def ffprobe(path:Path)->dict:
    return json.loads(subprocess.check_output(
        ['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

def verify_source(source:Path)->None:
    p=ffprobe(source)
    v=next((x for x in p['streams'] if x['codec_type']=='video'),None)
    a=next((x for x in p['streams'] if x['codec_type']=='audio'),None)
    if not v or not a or v['width']!=WIDTH or v['height']!=HEIGHT:
        raise ValueError('Requires 1080x1920 audiovisual source')
    if v['codec_name']!='h264' or a['codec_name']!='aac' or int(a['sample_rate'])!=48000:
        raise ValueError('Unexpected audiovisual source codecs')
    if abs(float(p['format']['duration'])-sum(FRAMES)/FPS)>0.05:
        raise ValueError('Unexpected source duration')

def run(source:Path,out:Path,genre:str,manifest:dict,
        transition_frames:int=TRANSITION_FRAMES)->Path:
    boundaries=validate(genre,manifest,transition_frames)
    source,out=Path(source),Path(out)
    if not source.is_file():raise FileNotFoundError(source)
    if source.resolve()==out.resolve():raise ValueError('Refusing source overwrite')
    verify_source(source)
    out.parent.mkdir(parents=True,exist_ok=True)
    l,t,r,b=PHOTO_RECT
    with tempfile.TemporaryDirectory(prefix='cycle838-local-') as tmp:
        stills=[]
        for i,cut in enumerate(boundaries):
            path=Path(tmp)/f'prior_scene_{i}.png'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                '-ss',f'{(cut-1)/FPS:.9f}','-i',str(source),
                '-frames:v','1','-vf',f'crop={r-l}:{b-t}:{l}:{t}',str(path)],check=True)
            stills.append(path)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
        for still in stills:
            cmd+=['-loop','1','-framerate',str(FPS),
                  '-t',f'{transition_frames/FPS:.9f}','-i',str(still)]
        cmd+=['-filter_complex',overlay_graph(boundaries,transition_frames),
              '-map','[vout]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
              '-crf','20','-pix_fmt','yuv420p','-r',str(FPS),
              '-frames:v',str(sum(FRAMES)),'-c:a','copy',
              '-movflags','+faststart',str(out)]
        subprocess.run(cmd,check=True)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--transition-frames',type=int,default=TRANSITION_FRAMES)
    a=p.parse_args()
    run(a.source,a.out,a.genre,json.loads(a.manifest.read_text()),a.transition_frames)
