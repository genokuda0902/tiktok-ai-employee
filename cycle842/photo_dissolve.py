"""cycle842: frame-exact masked photo dissolves, preserving Japanese ASS + AAC.
No uploads, paid services, publishing, or automatic posting. Human review only.
"""
from __future__ import annotations
import json, math, subprocess
from pathlib import Path

WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENE_LENGTHS = (89,81,79,87,86,89,77,103)
BOUNDARIES = tuple(sum(SCENE_LENGTHS[:i]) for i in range(1,8))
PHOTO_BOX = (30,350,1050,1300)
TRANSITION_FRAMES = 12
GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
POLICY = dict(review_only=True,publication_approved=False,automatic_posting=False,
              external_upload=False,source_rights_reviewed=False,contains_personal_data=False)

def check_manifest(manifest, genre):
    if genre not in GENRES or len(GENRES)!=10:
        raise ValueError('Unsupported genre')
    if any(manifest.get(k) is not v for k,v in POLICY.items()):
        raise ValueError('Fail closed: unsafe or missing review policy')

def easing(step, frames=TRANSITION_FRAMES):
    if frames<2 or frames%2 or not 0<=step<frames:
        raise ValueError('Invalid transition frame')
    x=(step+1)/(frames+1)
    return (1-math.cos(math.pi*x))/2

def timeline(scene_lengths=SCENE_LENGTHS, frames=TRANSITION_FRAMES):
    if frames<2 or frames%2 or len(scene_lengths)<2 or min(scene_lengths)<=frames:
        raise ValueError('Invalid transition setup')
    half=frames//2
    segments=[]
    for i,length in enumerate(scene_lengths):
        segments.append(('still',i,length-(half if i else 0)-
                         (half if i<len(scene_lengths)-1 else 0)))
        if i<len(scene_lengths)-1:
            segments.append(('dissolve',i,frames))
    if sum(s[2] for s in segments)!=sum(scene_lengths):
        raise AssertionError('Frame drift')
    return segments

def photo_mask():
    from PIL import Image,ImageDraw
    l,t,r,b=PHOTO_BOX;w,h=r-l,b-t
    mask=Image.new('L',(w,h),0);d=ImageDraw.Draw(mask)
    d.rounded_rectangle((6,6,w-7,h-7),radius=28,fill=255)
    d.rectangle((55-l,368-t,285-l,442-t),fill=0)  # STEP label stays fixed
    return mask

def transition_frame(previous, following, step, mask=None):
    from PIL import Image
    if previous.size!=(WIDTH,HEIGHT) or following.size!=(WIDTH,HEIGHT):
        raise ValueError('Source size mismatch')
    if mask is None:mask=photo_mask()
    l,t,r,b=PHOTO_BOX
    blended=Image.blend(previous.crop(PHOTO_BOX),following.crop(PHOTO_BOX),easing(step))
    base=(previous if step<TRANSITION_FRAMES//2 else following).copy()
    base.paste(blended,(l,t),mask)
    return base

def _run(cmd,timeout=180):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout)
    if p.returncode:
        raise RuntimeError(p.stderr[-2000:])
    return p

def _clip(inputs,frames,out):
    _run(['ffmpeg','-hide_banner','-loglevel','error','-y',*inputs,
          '-frames:v',str(frames),'-an','-c:v','libx264','-preset','ultrafast',
          '-crf','19','-pix_fmt','yuv420p','-r','30',str(out)])

def render(slides_dir,voice_mp4,captions_ass,output):
    """Use explicit 30fps scene clips; never use looped-PNG xfade timebase.
    Audio stream-copied bit-for-bit; 24 one-beat ASS captions overlaid last.
    """
    from PIL import Image
    slides_dir=Path(slides_dir);output=Path(output)
    slides=[Image.open(slides_dir/f'slide_{i:02d}.png').convert('RGB') for i in range(1,9)]
    temp=output.parent/'_segments';temp.mkdir(parents=True,exist_ok=True)
    mask=photo_mask();files=[]
    for index,(kind,scene,count) in enumerate(timeline()):
        clip=temp/f'clip_{index:02d}.mp4'
        if kind=='still':
            _clip(['-loop','1','-framerate','30','-i',
                   str(slides_dir/f'slide_{scene+1:02d}.png')],count,clip)
        else:
            frames_dir=temp/f'frames_{scene:02d}';frames_dir.mkdir(exist_ok=True)
            for step in range(TRANSITION_FRAMES):
                transition_frame(slides[scene],slides[scene+1],step,mask).save(
                    frames_dir/f'frame_{step:03d}.jpg',quality=91,subsampling=0)
            _clip(['-framerate','30','-start_number','0','-i',
                   str(frames_dir/'frame_%03d.jpg')],count,clip)
        files.append(clip)
    concat=temp/'clips.ffconcat'
    concat.write_text('ffconcat version 1.0\n'+''.join(
        f"file '{f.name}'\n" for f in files),encoding='utf-8')
    base=temp/'base.mp4'
    _run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat',
          '-safe','0','-i',str(concat),'-c:v','copy','-an',str(base)])
    ass=str(captions_ass).replace('\\','\\\\').replace(':','\\:').replace("'","\\'")
    _run(['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2',
          '-i',str(base),'-i',str(voice_mp4),
          '-vf',f'subtitles=filename={ass}:fontsdir=/usr/share/fonts/opentype/noto',
          '-map','0:v:0','-map','1:a:0','-c:v','libx264',
          '-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',
          '-r','30','-frames:v','691','-c:a','copy',
          '-movflags','+faststart',str(output)],timeout=300)
    return {'frames':691,'dissolves':7,'duration':691/30,
            'policy':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
