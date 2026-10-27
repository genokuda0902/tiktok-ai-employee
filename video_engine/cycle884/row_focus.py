"""Review-only row spotlight for a 10-genre video. No network, posting, or uploads."""
import argparse
import hashlib
import json
import subprocess
from bisect import bisect_right
from dataclasses import dataclass
from pathlib import Path

GENRES = ('ai_productivity','beauty','romance_psychology','money_saving',
          'sales_business','career','health_lifestyle','trivia_science',
          'travel_food','product_lifestyle')
WIDTH, HEIGHT, FPS, FRAMES, CAPTION_TOP = 1080, 1920, 30, 691, 1438
POLICY = dict(review_only=True, publication_approved=False, external_upload=False,
              automatic_posting=False, source_rights_reviewed=False)

@dataclass(frozen=True)
class Focus:
    frame: int
    box: tuple[int,int,int,int]

# For the private, fictional monthly-data demonstration in scene 01 only.
DEMO_STEPS = (Focus(18,(82,650,847,741)), Focus(36,(82,749,847,838)),
              Focus(54,(82,846,847,936)), Focus(78,(82,953,847,1052)))

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def validate(genre,steps=DEMO_STEPS,canvas=(WIDTH,HEIGHT),safe_top=CAPTION_TOP,total_frames=FRAMES):
    if genre not in GENRES: raise ValueError('unknown genre')
    w,h=canvas
    if not (w>0 and h>0 and 0<safe_top<h): raise ValueError('invalid canvas')
    if not steps or sorted({s.frame for s in steps})!=[s.frame for s in steps]:
        raise ValueError('steps must be strictly ordered')
    if any(s.frame<5 or s.frame>=total_frames-5 for s in steps):
        raise ValueError('step outside timeline')
    if any(b.frame-a.frame<10 for a,b in zip(steps,steps[1:])):
        raise ValueError('steps too close')
    for s in steps:
        x0,y0,x1,y1=s.box
        if not (24<=x0<x1<=w-24 and 30<=y0<y1<safe_top-40):
            raise ValueError('focus outside safe region')
    return True

def validate_manifest(manifest,source):
    if any(manifest.get(k) is not v for k,v in POLICY.items()):
        raise ValueError('unsafe review policy')
    if manifest.get('synthetic_ui') is not True or manifest.get('source_sha256')!=sha256(source):
        raise ValueError('unverified source/provenance')
    return True

def frame_overlay(n,steps=DEMO_STEPS,canvas=(WIDTH,HEIGHT),safe_top=CAPTION_TOP):
    """Transparent RGBA spotlight, always zero alpha at/under subtitle safe boundary."""
    from PIL import Image,ImageDraw
    im=Image.new('RGBA',canvas,(0,0,0,0))
    starts=[s.frame for s in steps]
    idx=bisect_right(starts,n)-1
    if idx<0: return im
    s=steps[idx]
    end=steps[idx+1].frame if idx+1<len(steps) else min(88,n+15)
    if n>=end:return im
    elapsed=n-s.frame
    fade_in=min(1.,(elapsed+1)/5)
    fade_out=min(1.,max(0,end-n)/4)
    a=round(215*min(fade_in,fade_out))
    if a==0:return im
    x0,y0,x1,y1=s.box
    # Draw only a thin animated perimeter; do not occlude the fictional source values.
    d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle((x0-5,y0-5,x1+5,y1+5),radius=20,
                        outline=(15,217,235,max(10,a//5)),width=12)
    d.rounded_rectangle((x0,y0,x1,y1),radius=15,
                        outline=(75,245,250,a),width=5)
    d.rounded_rectangle((x0-9,y0+12,x0-1,y1-12),radius=3,
                        fill=(255,211,102,round(a*.8)))
    # A short scanner travels over the top border; focal guidance, not a fake cursor.
    progress=min(1.,elapsed/12)
    scan_x=round(x0+15+(x1-x0-110)*progress)
    d.rounded_rectangle((scan_x,y0-7,scan_x+90,y0+2),radius=4,
                        fill=(255,220,123,a))
    return im

def create_overlays(folder,steps=DEMO_STEPS,count=89,canvas=(WIDTH,HEIGHT),safe_top=CAPTION_TOP):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    for n in range(count):
        frame_overlay(n,steps,canvas,safe_top).save(folder/f'{n:03d}.png',optimize=True)
    return count

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
      'format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames,sample_rate',
      '-of','json',str(path)]))

def render(source,output,manifest_path,report_path,genre='ai_productivity',work_dir=None):
    validate(genre)
    source=Path(source);output=Path(output)
    manifest=json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    validate_manifest(manifest,source)
    p=probe(source)
    v=next(s for s in p['streams'] if s['codec_type']=='video')
    a=next(s for s in p['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],int(v.get('nb_frames') or 0),a['codec_name']) != (WIDTH,HEIGHT,'30/1',FRAMES,'aac'):
        raise ValueError('source does not match approved review baseline')
    output.parent.mkdir(parents=True,exist_ok=True)
    frames_dir=Path(work_dir or output.parent/'private_overlays')
    create_overlays(frames_dir)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate','30','-start_number','0','-i',str(frames_dir/'%03d.png'),
         '-filter_complex',"[0:v][1:v]overlay=x=0:y=0:shortest=0:format=auto:enable='lt(n,89)'[v]",
         '-map','[v]','-map','0:a:0','-frames:v',str(FRAMES),'-c:v','libx264',
         '-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy',
         '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=300)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),
                    '-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,timeout=120)
    q=probe(output)
    report={'cycle':884,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'genre':genre,'focus_frames':[s.frame for s in DEMO_STEPS],
            'focus_boxes':[s.box for s in DEMO_STEPS],
            'resolution':[WIDTH,HEIGHT],'duration':q['format']['duration'],
            'streams':q['streams'],'full_av_decode':'PASS',
            'voice_transcription':'UNVERIFIED','semantic_caption_sync':'UNVERIFIED',
            'rights':'UNVERIFIED','smartphone':'UNVERIFIED',
            'quality_gate':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    Path(report_path).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for arg in ('source','output','manifest','report'):ap.add_argument('--'+arg,required=True)
    ap.add_argument('--genre',default='ai_productivity')
    ap.add_argument('--work-dir')
    x=ap.parse_args()
    print(json.dumps(render(x.source,x.output,x.manifest,x.report,x.genre,x.work_dir),ensure_ascii=False,indent=2))
