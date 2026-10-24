"""Review-only photo-led insert; captions/audio retained, no publishing.
Requires explicit provenance for internal review. No rights inferred for posting.
"""
from __future__ import annotations
import argparse,json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageOps

GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business',
        'career','health_life','science','travel_food','product_life')
ALLOWED_ORIGINS=('user_conversation_generated','procedural_original')
SAFE_IMAGE_BOX=(64,655,952,470)

def validate_manifest(path:Path,genre:str)->dict:
    if genre not in GENRES:raise ValueError('unknown genre')
    data=json.loads(path.read_text(encoding='utf-8'))
    if data.get('origin') not in ALLOWED_ORIGINS:
        raise PermissionError('asset origin not allowlisted')
    if data.get('review_allowed') is not True or data.get('private_data') is not False:
        raise PermissionError('internal review permission/privacy gate failed')
    if data.get('publication_approved') is not False:
        raise PermissionError('review-only asset cannot be marked publication-approved')
    x,y,w,h=SAFE_IMAGE_BOX
    if x<0 or y<0 or x+w>1080 or y+h>1150:
        raise ValueError('caption-safe region violation')
    return data

def make_filter(start:float,duration:float)->str:
    if start<0 or duration<1.0 or start+duration>60:
        raise ValueError('invalid scene timing')
    x,y,w,h=SAFE_IMAGE_BOX
    enabled=f'between(t,{start:.3f},{start+duration:.3f})'
    return (f"[0:v][1:v]overlay=x={x}:y={y}:shortest=1:enable='{enabled}',"
            f"drawbox=x={x}:y={y}:w={w}:h={h}:color=white@0.9:t=5:enable='{enabled}',"
            'format=yuv420p[out]')

def render(source:Path,image:Path,manifest:Path,output:Path,genre:str,start:float,duration:float)->dict:
    validate_manifest(manifest,genre)
    if not source.is_file() or not image.is_file():
        raise FileNotFoundError('source MP4 or image missing')
    output.parent.mkdir(parents=True,exist_ok=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error',
      '-show_streams','-show_format','-of','json',str(source)]))
    video=next(x for x in probe['streams'] if x['codec_type']=='video')
    video_duration=float(probe['format']['duration'])
    frames=int(video['nb_frames'])
    if start+duration>video_duration+0.02:
        raise ValueError('scene extends past source video')
    with tempfile.TemporaryDirectory(prefix='cycle825_') as td:
        photo=Path(td)/'review_photo.png'
        with Image.open(image) as im:
            ImageOps.fit(im.convert('RGB'),(SAFE_IMAGE_BOX[2],SAFE_IMAGE_BOX[3]),
                         method=Image.Resampling.LANCZOS,centering=(0.5,0.38)).save(photo)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-loop','1','-framerate','30','-i',str(photo),'-filter_complex',make_filter(start,duration),
             '-map','[out]','-map','0:a:0','-t',f'{video_duration:.6f}',
             '-frames:v',str(frames),'-c:v','libx264','-preset','ultrafast',
             '-crf','21','-threads','4','-pix_fmt','yuv420p','-c:a','copy',
             '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True)
    return {'genre':genre,'scene_seconds':[start,start+duration],
            'caption_safe':True,'audio_stream_copied':True,'review_only':True,
            'publication_approved':False,'auto_post':False,'output':str(output)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('source','image','manifest','output'):
        p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--genre',choices=GENRES,required=True)
    p.add_argument('--start',type=float,default=6.47)
    p.add_argument('--duration',type=float,default=2.98)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.image,a.manifest,a.output,a.genre,a.start,a.duration),ensure_ascii=False,indent=2))
