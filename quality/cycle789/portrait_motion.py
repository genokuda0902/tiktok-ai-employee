#!/usr/bin/env python3
"""Review-only, genre-neutral Ken Burns motion in photo panels; NEVER posts.

Only pixels within configured photographic regions are altered. Source is an
already rendered local review video; input images/audio must have separate
human rights/privacy review before any external publication.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

W, H, FPS = 1080, 1920, 30

def smoothstep(x):
    x = max(0.0, min(1.0, float(x)))
    return x*x*(3.0-2.0*x)

def fade(t, start, end, edge=0.25):
    if not start <= t <= end:
        return 0.0
    return min(smoothstep((t-start)/edge), smoothstep((end-t)/edge))

def validate(c):
    if c.get('mode') != 'review_only' or c.get('publication_approved') is not False or c.get('rights_reviewed') is not False:
        raise ValueError('Fail closed: REVIEW_ONLY and unapproved flags required')
    if c.get('canvas') != [W,H] or c.get('fps') != FPS:
        raise ValueError('1080x1920 at 30fps required')
    if not 1 <= len(c.get('regions',[])) <= 8:
        raise ValueError('1..8 photo regions required')
    for r in c['regions']:
        x0,y0,x1,y1 = r['box']
        if not (55 <= x0 < x1 <= W-55 and 210 <= y0 < y1 <= H-270):
            raise ValueError('Unsafe photo region')
        if not (0.0 <= r['start'] < r['end'] <= 25.0):
            raise ValueError('Invalid time range')
        if not (r['start'] < r['source_time'] < r['end']):
            raise ValueError('Reference frame must be inside scene')
        if not (1.0 <= r['zoom_from'] <= 1.08 and 1.0 <= r['zoom_to'] <= 1.08):
            raise ValueError('Maximum safe zoom is 8%')
        if not (-0.025 <= r['pan_x'] <= 0.025 and -0.025 <= r['pan_y'] <= 0.025):
            raise ValueError('Maximum pan 2.5%')
        if r.get('fade_seconds',.22) < .15:
            raise ValueError('Require smooth in/out fade')
    return True

def edge_blend(distance, feather=22):
    """Smoothly blend the transformed photo back into its unmodified panel border."""
    return smoothstep(float(distance)/float(feather))

def crop_zoom(image, zoom, pan_x=0., pan_y=0.):
    """Returns PIL RGB image, exactly same size, with subtle center-cropped motion."""
    from PIL import Image
    w,h=image.size
    if not 1 <= zoom <= 1.08:
        raise ValueError('Zoom out of bounds')
    cw,ch=max(1,round(w/zoom)),max(1,round(h/zoom))
    dx=round(pan_x*(w-cw));dy=round(pan_y*(h-ch))
    x=max(0,min(w-cw,(w-cw)//2+dx));y=max(0,min(h-ch,(h-ch)//2+dy))
    return image.crop((x,y,x+cw,y+ch)).resize((w,h),Image.Resampling.BICUBIC)

def ffprobe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def render(source, dest, config, report):
    import cv2
    import numpy as np
    from PIL import Image
    c=json.loads(Path(config).read_text(encoding='utf-8'))
    validate(c)
    source,dest=Path(source),Path(dest)
    if not source.is_file(): raise FileNotFoundError(source)
    meta=ffprobe(source)
    vs=next(s for s in meta['streams'] if s['codec_type']=='video')
    if (vs['width'],vs['height']) != (W,H) or vs['codec_name']!='h264':
        raise ValueError('Source must be H.264 1080x1920')
    if not any(s['codec_type']=='audio' and s['codec_name']=='aac' for s in meta['streams']):
        raise ValueError('AAC narration source required')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError('Cannot decode source')
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if count < 1: raise ValueError('No video frames')
    stills=[]
    blend_masks=[]
    for r in c['regions']:
        cap.set(cv2.CAP_PROP_POS_FRAMES,round(r['source_time']*FPS))
        ok,frame=cap.read()
        if not ok: raise RuntimeError('Reference frame missing')
        x0,y0,x1,y1=r['box']
        stills.append(Image.fromarray(cv2.cvtColor(frame[y0:y1,x0:x1],cv2.COLOR_BGR2RGB)))
        h,w=y1-y0,x1-x0
        yy,xx=np.ogrid[:h,:w]
        dist=np.minimum(np.minimum(xx,w-1-xx),np.minimum(yy,h-1-yy)).astype(np.float32)
        z=np.clip(dist/22.,0.,1.)
        blend_masks.append(z*z*(3.-2.*z))
    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    dest.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0',
         '-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(dest)]
    enc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    frames=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            t=frames/FPS
            for r,still,blend in zip(c['regions'],stills,blend_masks):
                a=fade(t,r['start'],r['end'],r.get('fade_seconds',.22))
                if a < 1e-6:continue
                x0,y0,x1,y1=r['box']; progress=smoothstep((t-r['start'])/(r['end']-r['start']))
                z=r['zoom_from']+(r['zoom_to']-r['zoom_from'])*progress
                pan=r['pan_x']*(2*progress-1);py=r['pan_y']*(2*progress-1)
                transformed=np.asarray(crop_zoom(still,z,pan,py))
                bgr=cv2.cvtColor(transformed,cv2.COLOR_RGB2BGR)
                orig=frame[y0:y1,x0:x1]
                weight=(a*blend)[...,None]
                orig[:]=np.clip(bgr.astype(np.float32)*weight + orig.astype(np.float32)*(1.-weight),0,255).astype(np.uint8)
            try:enc.stdin.write(frame.tobytes())
            except BrokenPipeError: raise RuntimeError('ffmpeg encoder terminated')
            frames+=1
        enc.stdin.close()
        error=enc.stderr.read().decode('utf-8',errors='replace')
        ret=enc.wait()
        if ret:raise RuntimeError(f'ffmpeg exit {ret}: {error[-3000:]}')
    finally:
        cap.release()
        if enc.poll() is None:enc.kill()
    if frames != count:raise RuntimeError(f'Frame count mismatch: {frames} vs {count}')
    info=ffprobe(dest)
    out_v=next(s for s in info['streams'] if s['codec_type']=='video')
    out_a=next(s for s in info['streams'] if s['codec_type']=='audio')
    if (out_v['width'],out_v['height'])!=(W,H) or out_v['codec_name']!='h264' or out_a['codec_name']!='aac':
        raise RuntimeError('Unexpected output codecs')
    result={'cycle':789,'status':'HUMAN_REVIEW','publication_approved':False,'input':str(source),
            'output':str(dest),'genre':c.get('genre','ai_productivity'),
            'regions':len(c['regions']),'frame_count':frames,
            'duration':float(info['format']['duration']),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
            'quality_delta':'subtle Ken Burns motion inside two existing photo panels; text and audio retained',
            'caveats':['source rights unverified','Japanese speech semantic content not transcribed','smartphone test pending','no publication']}
    Path(report).parent.mkdir(parents=True,exist_ok=True)
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for arg in ('input','output','config','report'):p.add_argument('--'+arg,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output,a.config,a.report),ensure_ascii=False))
