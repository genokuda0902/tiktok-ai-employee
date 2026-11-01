"""Review-only opening camera motion for a locally supplied, SHA-pinned MP4.

Reimplementation, not the original v33 source.  The hook picture is pushed
in gently without modifying the title, narration, or burnt-in Japanese
captions.  The renderer uses only the local source; no media is committed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

FPS = 30
ROI = (90, 390, 900, 750)  # x, y, width, height
HOOK = (0, 45)             # actual robot hook only, before 1.5s montage cut
CAPTION_START_Y = 1490
PALETTES = {
    'ai_work':'#36d9dc','money':'#f1c267','career':'#75baf7',
    'business':'#6ed9ae','health':'#ffa09b','study':'#b7a5f8',
    'lifestyle':'#f5add4','technology':'#66d7fc','travel':'#ffcf8d',
    'mindset':'#a6e7be',
}


def sha256(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):
            h.update(block)
    return h.hexdigest()


def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError(f'{cmd[0]} exited {p.returncode}: {p.stderr[-1800:]}')
    return p.stdout


def validate(m):
    if set(m) != {'genre','synthetic_scenario','review_only','rights_status',
                  'contains_private_data','zoom_max','focus_x','focus_y'}:
        raise ValueError('unexpected/missing manifest fields')
    if m['genre'] not in PALETTES:
        raise ValueError('unsupported genre')
    if (m['synthetic_scenario'] is not True or m['review_only'] is not True
        or m['rights_status']!='unverified' or m['contains_private_data'] is not False):
        raise ValueError('release/rights/privacy gate: review-only synthetic scenario required')
    if type(m['zoom_max']) not in (float,int) or not 1.02<=m['zoom_max']<=1.14:
        raise ValueError('zoom_max out of cinematic range')
    for k in ('focus_x','focus_y'):
        if type(m[k]) not in (float,int) or not 0.4<=m[k]<=0.6:
            raise ValueError('focus center must stay inside protected ROI')
    x,y,w,h=ROI
    if x<0 or y<0 or x+w>1080 or y+h>=CAPTION_START_Y:
        raise ValueError('overlay would collide with title/subtitle')
    return True


def ease(t):
    t=max(0.0,min(1.0,t))
    return t*t*(3-2*t)


def camera_params(frame,total,m):
    validate(m)
    if type(frame) is not int or not 0<=frame<total or total<2:
        raise ValueError('frame outside hook')
    # One smooth push-in; no fake jump cuts or misleading UI alterations.
    t=ease(frame/(total-1))
    return 1.0+(m['zoom_max']-1.0)*t, 8.0*t, -6.0*t


def motion_frame(base,frame,total,m,edge_mask=None):
    if base.size != ROI[2:]:
        raise ValueError('incorrect source crop dimensions')
    zoom,dx,dy=camera_params(frame,total,m)
    w,h=base.size
    nw,nh=round(w*zoom),round(h*zoom)
    big=base.resize((nw,nh),Image.Resampling.LANCZOS)
    cx=m['focus_x']*nw+dx
    cy=m['focus_y']*nh+dy
    left=round(cx-m['focus_x']*w)
    top=round(cy-m['focus_y']*h)
    left=max(0,min(left,nw-w));top=max(0,min(top,nh-h))
    transformed=big.crop((left,top,left+w,top+h))
    if edge_mask is None:
        edge_mask=feather_mask(w,h)
    return Image.composite(transformed,base,edge_mask)


def feather_mask(w,h):
    # Mask has zero opacity at every ROI boundary; surrounding UI remains fixed.
    mask=Image.new('L',(w,h),0)
    d=ImageDraw.Draw(mask)
    d.rectangle((55,55,w-56,h-56),fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(22))
    ImageDraw.Draw(mask).rectangle((0,0,w-1,h-1),outline=0,width=8)
    return mask


def make_overlay_sequence(source,directory,total,m):
    x,y,w,h=ROI
    cmd=['ffmpeg','-v','error','-i',str(source),'-vf',
         f'crop={w}:{h}:{x}:{y}', '-frames:v',str(total),
         '-pix_fmt','rgb24','-f','rawvideo','pipe:1']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    size=w*h*3
    mask=feather_mask(w,h)
    try:
        for i in range(total):
            raw=bytearray()
            while len(raw)<size:
                part=p.stdout.read(size-len(raw))
                if not part:
                    raise RuntimeError(f'ffmpeg source ended at frame {i}')
                raw.extend(part)
            base=Image.frombytes('RGB',(w,h),bytes(raw))
            frame=motion_frame(base,i,total,m,mask)
            frame.save(Path(directory)/f'overlay_{i:03d}.png',compress_level=1)
        p.stdout.close()
        if p.wait()!=0:
            raise RuntimeError('ffmpeg crop decoder failed')
    finally:
        if p.poll() is None:
            p.kill();p.wait()


def render(source,out,expected_sha,m,start=HOOK[0],end=HOOK[1]):
    validate(m)
    if len(expected_sha)!=64 or sha256(source)!=expected_sha:
        raise ValueError('source SHA256 mismatch: fail closed')
    meta=json.loads(run(['ffprobe','-v','error','-show_streams',
                         '-show_format','-of','json',str(source)]))
    vs=[s for s in meta['streams'] if s['codec_type']=='video']
    au=[s for s in meta['streams'] if s['codec_type']=='audio']
    if (len(vs)!=1 or len(au)!=1 or
        (vs[0]['codec_name'],vs[0]['width'],vs[0]['height'],vs[0]['r_frame_rate'])
         !=('h264',1080,1920,'30/1') or
        (au[0]['codec_name'],au[0]['sample_rate'])!=('aac','48000')):
        raise ValueError('source must be 1080x1920 30fps H264 and 48k AAC')
    frames=int(vs[0].get('nb_frames') or round(float(meta['format']['duration'])*FPS))
    if not 0<=start<end<=frames or end-start>90:
        raise ValueError('hook window outside video or too long')
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        make_overlay_sequence(source,tmp,end-start,m)
        x,y,w,h=ROI
        graph=(f'[1:v]setpts=PTS-STARTPTS+{start/FPS}/TB[ov];'
               f"[0:v][ov]overlay={x}:{y}:eof_action=pass:repeatlast=0:"
               f"enable='between(n,{start},{end-1})'[v]")
        run(['ffmpeg','-v','error','-y','-i',str(source),
             '-framerate',str(FPS),'-i',f'{tmp}/overlay_%03d.png',
             '-filter_complex',graph,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','19',
             '-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy',
             '-movflags','+faststart',str(out)])
    run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
    return {'source_sha256':expected_sha,'output_sha256':sha256(out),
            'changed_frames':[start,end-1], 'max_zoom':m['zoom_max'],
            'genre':m['genre'], 'audio':'AAC stream copy',
            'caption_policy':f'no overlay at y >= {CAPTION_START_Y}',
            'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


def smoke():
    with tempfile.TemporaryDirectory() as tmp:
        src=Path(tmp)/'synthetic.mp4';out=Path(tmp)/'out.mp4'
        run(['ffmpeg','-v','error','-y','-f','lavfi','-i',
             'testsrc2=s=1080x1920:r=30:d=2','-f','lavfi','-i',
             'sine=frequency=330:sample_rate=48000:duration=2',
             '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
             '-c:a','aac','-shortest',str(src)])
        m=json.loads((Path(__file__).parent/'manifest.json').read_text())
        print(json.dumps(render(src,out,sha256(src),m,0,36),ensure_ascii=False))
        print('PASS: synthetic 2s A/V fully decoded')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source');p.add_argument('--source-sha')
    p.add_argument('--manifest');p.add_argument('--out');p.add_argument('--smoke',action='store_true')
    a=p.parse_args()
    if a.smoke:smoke()
    else:
        if not all([a.source,a.source_sha,a.manifest,a.out]):p.error('missing render arguments')
        m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
        print(json.dumps(render(a.source,a.out,a.source_sha,m),ensure_ascii=False,indent=2))
