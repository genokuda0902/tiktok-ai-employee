"""cycle840: Photo-only dissolves on repaired Japanese narration. Review-only."""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

FPS=30
WIDTH,HEIGHT=1080,1920
ORIGINAL_SCENES=(101,93,91,99,98,101,89,103)
REMOVED_PER_BOUNDARY=12
PHOTO_RECT=(62,390,1018,1390)
DISSOLVE_FRAMES=8
GENRES=('ai_work','sales_business','beauty','romance','saving',
        'career','wellness','science','travel_food','productivity')
REQUIRED={'data_classification':'fictional','contains_personal_data':False,
          'review_only':True,'publication_approved':False,
          'source_rights_reviewed':False,'external_upload':False,
          'automatic_posting':False}

def boundaries(original=ORIGINAL_SCENES,removed=REMOVED_PER_BOUNDARY):
    if len(original)!=8 or any(n<30 for n in original):
        raise ValueError('Eight scenes required')
    if type(removed) is not int or not 0<=removed<=15:
        raise ValueError('Invalid trim')
    return tuple(sum(original[:i])-removed*i for i in range(1,8))

def check_policy(manifest,genre,dissolve_frames=DISSOLVE_FRAMES):
    if not isinstance(manifest,dict) or any(manifest.get(k)!=v for k,v in REQUIRED.items()):
        raise ValueError('Fail closed: fictional human-review-only source required')
    if genre not in GENRES or len(GENRES)!=10:
        raise ValueError('Unsupported genre')
    if type(dissolve_frames) is not int or not 3<=dissolve_frames<=12:
        raise ValueError('Dissolve length must be 3..12 frames')
    l,t,r,b=PHOTO_RECT
    if not (0<=l<r<=WIDTH and 0<=t<b<1395):
        raise ValueError('Photo area overlaps subtitle region')
    return boundaries()

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error',
        '-show_streams','-show_format','-of','json',str(path)],text=True))

def check_source(path):
    info=probe(path)
    video=next((s for s in info['streams'] if s['codec_type']=='video'),None)
    audio=next((s for s in info['streams'] if s['codec_type']=='audio'),None)
    if not video or not audio:
        raise ValueError('Source requires video and audio')
    if (video['codec_name'],video['width'],video['height'])!=('h264',WIDTH,HEIGHT):
        raise ValueError('Requires H264 1080x1920')
    if audio['codec_name']!='aac' or int(audio['sample_rate'])!=48000:
        raise ValueError('Requires AAC 48kHz')
    if abs(float(video['duration'])-691/FPS)>.06:
        raise ValueError('Requires 691-frame cycle839 source')
    if float(audio['duration'])<float(video['duration'])-.10:
        raise ValueError('Refusing silent output: insufficient audio coverage')
    return info

def filter_graph(cuts,dissolve_frames=DISSOLVE_FRAMES):
    l,t,r,b=PHOTO_RECT
    chain=[]
    prev='0:v'
    for i,cut in enumerate(cuts,1):
        chain.append(f'[{i}:v]format=rgba,fade=t=out:st=0:d={dissolve_frames/FPS:.9f}:alpha=1,'
                     f'setpts=PTS-STARTPTS+{cut}/({FPS}*TB)[photo{i}]')
        chain.append(f'[{prev}][photo{i}]overlay={l}:{t}:eof_action=pass:repeatlast=0:format=auto[v{i}]')
        prev=f'v{i}'
    chain.append(f'[{prev}]format=yuv420p[vout]')
    return ';'.join(chain)

def render(source,output,manifest,genre='ai_work',dissolve_frames=DISSOLVE_FRAMES):
    cuts=check_policy(manifest,genre,dissolve_frames)
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve():raise ValueError('Refuse overwrite')
    check_source(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    l,t,r,b=PHOTO_RECT
    with tempfile.TemporaryDirectory(prefix='cycle840-') as td:
        stills=[]
        for i,cut in enumerate(cuts):
            still=Path(td)/f'previous_photo_{i+1}.png'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                '-ss',f'{(cut-1)/FPS:.9f}','-i',str(source),
                '-frames:v','1','-vf',f'crop={r-l}:{b-t}:{l}:{t}',
                str(still)],check=True,timeout=25)
            stills.append(still)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-filter_complex_threads','2','-threads','2','-i',str(source)]
        for still in stills:
            cmd+=['-loop','1','-framerate',str(FPS),'-t',
                  f'{dissolve_frames/FPS:.9f}','-i',str(still)]
        cmd+=['-filter_complex',filter_graph(cuts,dissolve_frames),
              '-map','[vout]','-map','0:a:0','-c:v','libx264',
              '-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',
              '-r',str(FPS),'-frames:v','691','-c:a','copy',
              '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=240)
    check_source(output)
    return {'boundaries_frames':cuts,'photo_rect':PHOTO_RECT,
            'dissolve_frames':dissolve_frames,'audio_processing':'stream_copy',
            'genre':genre,'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--frames',type=int,default=DISSOLVE_FRAMES)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(a.manifest.read_text()),
                            a.genre,a.frames),ensure_ascii=False,indent=2))
