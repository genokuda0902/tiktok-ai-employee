#!/usr/bin/env python3
"""Zero-cost, genre-agnostic circular replay-loop bridge, review-only.

The last 18 video frames reveal the *actual first frame* in the picture area,
so a TikTok loop no longer jumps from the outro card to the opening robot.
The original burned Japanese captions (y >= 1280) and AAC are untouched.
Private source remains local; no private frames/audio are uploaded to GitHub.
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image

W, H, FPS, FRAMES = 1080, 1920, 30, 691
PROTECTED_Y = 1280
BRIDGE_FRAMES = 18
START_FRAME = FRAMES - BRIDGE_FRAMES
SOURCE_SHA = '2bf5b682b427da56ce87ce0ea41e07c99298b1d42aa97ab1c21acd185cb02b1d'
GENRES = ('ai_work','beauty','romance_psychology','money_saving','sales_business',
          'career','health_lifestyle','science_trivia','travel_food','product_comparison_lifestyle')


def run(args, binary=False):
    p = subprocess.run([str(a) for a in args], capture_output=True)
    if p.returncode:
        raise RuntimeError(f'{args[0]} failed: {p.stderr.decode(errors="replace")[-1800:]}')
    return p.stdout if binary else p.stdout.decode()


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))


def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0',
                               '-c','copy','-f','adts','-'],binary=True)).hexdigest()


def frame_image(path, n):
    raw=run(['ffmpeg','-v','error','-i',path,'-vf',f'select=eq(n\\,{n})',
             '-frames:v','1','-f','image2pipe','-vcodec','png','-'],binary=True)
    return Image.open(io.BytesIO(raw)).convert('RGB')


def validate_source(path, expected_sha, genre, review_only):
    if not review_only: raise ValueError('human-review-only flag required')
    if genre not in GENRES: raise ValueError('unknown genre')
    if genre!='ai_work': raise ValueError('no approved private source for this genre')
    if expected_sha != SOURCE_SHA or sha256(path) != SOURCE_SHA:
        raise ValueError('SHA-locked private source mismatch')
    p=probe(path)
    v=[x for x in p['streams'] if x['codec_type']=='video']
    a=[x for x in p['streams'] if x['codec_type']=='audio']
    if len(p['streams'])!=2 or len(v)!=1 or len(a)!=1: raise ValueError('exactly one video and audio required')
    if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],
        int(v[0]['nb_frames']),a[0]['codec_name'],int(a[0]['sample_rate'])) != \
       ('h264',W,H,'30/1',FRAMES,'aac',48000):
        raise ValueError('unexpected media profile')
    return p


def radial_mask(frame_index, width=W, height=PROTECTED_Y):
    """Deterministic soft radial wipe: 0 at start, opaque at final frame."""
    if not 0 <= frame_index < BRIDGE_FRAMES: raise ValueError('frame index out of range')
    if frame_index == 0: return np.zeros((height,width),dtype=np.uint8)
    if frame_index == BRIDGE_FRAMES-1: return np.full((height,width),255,dtype=np.uint8)
    progress=frame_index/(BRIDGE_FRAMES-1)
    smooth=progress*progress*(3-2*progress)
    yy,xx=np.ogrid[:height,:width]
    radius=np.sqrt((xx-width/2)**2+(yy-height/2)**2)
    corner=math.hypot(width/2,height/2)
    threshold=smooth*(corner+95)-48
    alpha=np.clip((threshold+48-radius)/96,0,1)
    return np.uint8(np.rint(alpha*255))


def create_overlays(first_frame, outdir):
    first=np.asarray(first_frame.crop((0,0,W,PROTECTED_Y)).convert('RGB'))
    outdir.mkdir(parents=True,exist_ok=True)
    for i in range(BRIDGE_FRAMES):
        rgba=np.empty((PROTECTED_Y,W,4),dtype=np.uint8)
        rgba[:,:,:3]=first
        rgba[:,:,3]=radial_mask(i)
        Image.fromarray(rgba,'RGBA').save(outdir/f'{i:03d}.png')


def render(source, dest, report, genre='ai_work', expected_sha=SOURCE_SHA, review_only=False):
    source,dest,report=map(Path,(source,dest,report))
    if len({source.resolve(),dest.resolve(),report.resolve()})!=3 or dest.exists() or report.exists():
        raise ValueError('paths must be distinct and output paths must not exist')
    validate_source(source,expected_sha,genre,review_only)
    first=frame_image(source,0)
    last_before=frame_image(source,FRAMES-1)
    dest.parent.mkdir(parents=True,exist_ok=True)
    report.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle1044_loop_') as t:
        overlays=Path(t)/'overlays'
        create_overlays(first,overlays)
        run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y',
             '-i',source,'-framerate',str(FPS),'-i',overlays/'%03d.png',
             '-filter_complex',f'[1:v]setpts=PTS+{START_FRAME}/({FPS}*TB)[wipe];'
                               '[0:v][wipe]overlay=0:0:eof_action=pass:format=auto[v]',
             '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
             '-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p',
             '-frames:v',str(FRAMES),'-c:a','copy','-metadata:s:a:0','language=jpn',
             '-movflags','+faststart',dest])
    run(['ffmpeg','-v','error','-xerror','-i',dest,'-f','null','-'])
    p=probe(dest)
    v=next(x for x in p['streams'] if x['codec_type']=='video')
    if (v['width'],v['height'],int(v['nb_frames'])) != (W,H,FRAMES):
        raise RuntimeError('unexpected output dimensions or frame count')
    if audio_sha(source)!=audio_sha(dest): raise RuntimeError('original AAC changed')
    last_after=frame_image(dest,FRAMES-1)
    a=np.asarray(first.crop((0,0,W,PROTECTED_Y)),dtype=np.int16)
    before=np.asarray(last_before.crop((0,0,W,PROTECTED_Y)),dtype=np.int16)
    after=np.asarray(last_after.crop((0,0,W,PROTECTED_Y)),dtype=np.int16)
    original_mae=float(np.abs(a-before).mean())
    new_mae=float(np.abs(a-after).mean())
    if not new_mae < original_mae*.10:
        raise RuntimeError(f'loop seam insufficient improvement: {new_mae} vs {original_mae}')
    result={
        'source_sha256':SOURCE_SHA,'output_sha256':sha256(dest),
        'transition_frames':[START_FRAME,FRAMES-1],
        'transition_seconds':[START_FRAME/FPS,FRAMES/FPS],
        'picture_only':'y=0..1279; burned captions y>=1280 protected',
        'first_last_picture_mae_before':round(original_mae,4),
        'first_last_picture_mae_after':round(new_mae,4),
        'full_av_decode':'PASS','duration_seconds':float(p['format']['duration']),
        'video':'H264 1080x1920 30fps','frames':FRAMES,
        'audio':'AAC 48kHz Japanese tagged; original elementary stream unchanged',
        'audio_adts_sha256':audio_sha(dest),
        'independent_japanese_asr':'NOT_VERIFIED',
        'speech_caption_semantics':'NOT_VERIFIED',
        'asset_publication_rights':'NOT_VERIFIED',
        'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('source','dest','report'): ap.add_argument('--'+name,required=True)
    ap.add_argument('--genre',default='ai_work')
    ap.add_argument('--expected-sha',default=SOURCE_SHA)
    ap.add_argument('--review-only',action='store_true')
    x=ap.parse_args()
    print(json.dumps(render(x.source,x.dest,x.report,x.genre,x.expected_sha,x.review_only),ensure_ascii=False))
