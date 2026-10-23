"""Rights-gated, 10-genre reusable first-3.2s kinetic hook.

Never uploads inherited video/photo/voice to GitHub. CI uses a synthetic frame.
"""
import argparse
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

WIDTH, HEIGHT, FPS, NFRAMES = 1080, 1920, 30, 96
LEFT_CARD = (61, 546, 397, 1001)
RIGHT_CARD = (432, 546, 769, 1001)
PHOTO_ROI = (69, 619, 390, 900)
SHEET_ROI = (440, 619, 760, 899)


def validate(cfg):
    if cfg.get('mode') != 'review_only':
        raise ValueError('Only review-only mode allowed')
    for key in ('rights_reviewed', 'employee_approved', 'publication_approved'):
        if cfg.get(key) is not False:
            raise ValueError(f'{key} must remain false')
    genres = cfg.get('genres')
    if not isinstance(genres, list) or len(genres) != 10 or len(set(genres)) != 10:
        raise ValueError('Exactly 10 unique genres required')
    if cfg.get('fps') != FPS or cfg.get('frame_count') != NFRAMES:
        raise ValueError('30fps/96-frame hook contract')
    if cfg.get('safe_margin_px', 0) < 48:
        raise ValueError('Safe margin too small')
    return True


def ease(t):
    t = max(0., min(1., t))
    return t*t*(3-2*t)


def synthetic_source():
    """Original abstract test plate, never user media."""
    im = Image.new('RGB', (WIDTH, HEIGHT), '#06192d')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(LEFT_CARD, radius=24, fill='#163c50', outline='#d6a48f', width=7)
    d.rounded_rectangle(RIGHT_CARD, radius=24, fill='#184d57', outline='#59eadc', width=7)
    for x in range(90, 390, 30):
        d.line((x, 650, x, 865), fill='#1e6683', width=5)
    for i in range(4):
        y=640+i*60
        d.rectangle((462,y,738,y+34), fill=('#d5eff0' if i%2==0 else '#a4d5db'))
    d.rounded_rectangle((60, 1140, 770, 1260), radius=20, fill='#124b5a')
    return im


def extract_first_frame(video):
    command = ['ffmpeg','-hide_banner','-loglevel','error','-ss','0.60','-i',str(video),
               '-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1']
    p = subprocess.run(command, capture_output=True, check=True)
    import io
    im = Image.open(io.BytesIO(p.stdout)).convert('RGB')
    if im.size != (WIDTH,HEIGHT):
        raise ValueError('Expected 1080x1920 source')
    return im


def roi_zoom(frame, roi, progress):
    """Subtle Ken Burns confined to an existing card; no text outside card is cropped."""
    x0,y0,x1,y1=roi
    src=frame.crop(roi)
    zoom=1.0 + 0.034 * ease(progress)
    w,h=src.size
    nw,nh=round(w*zoom),round(h*zoom)
    enlarged=src.resize((nw,nh),Image.Resampling.BICUBIC)
    ox=(nw-w)//2;oy=(nh-h)//2
    frame.paste(enlarged.crop((ox,oy,ox+w,oy+h)),(x0,y0))


def render_frame(source, index):
    if not 0 <= index < NFRAMES:
        raise ValueError('frame index')
    frame=source.copy()
    # 0.3–1.55s BEFORE; 1.55–2.85s AFTER; final 0.35s returns to both.
    sec=index/FPS
    left_weight=ease((sec-.30)/.28)*(1-ease((sec-1.47)/.22))
    right_weight=ease((sec-1.48)/.25)*(1-ease((sec-2.77)/.25))
    if left_weight>0.001:
        roi_zoom(frame,PHOTO_ROI,min(1.,(sec-.3)/1.0))
    if right_weight>0.001:
        roi_zoom(frame,SHEET_ROI,min(1.,(sec-1.48)/1.0))
    # Paint glow in a transparent layer and composite it under a sharp outline.
    overlay=Image.new('RGBA',frame.size,(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    for box,color,weight in [(LEFT_CARD,(255,155,114),left_weight),(RIGHT_CARD,(45,238,222),right_weight)]:
        if weight<0.01: continue
        pulse=0.8+0.2*math.sin(index*.22)
        alpha=round(105*weight*pulse)
        d.rounded_rectangle(box,radius=27,outline=(*color,alpha),width=12)
    glow=overlay.filter(ImageFilter.GaussianBlur(21))
    frame=Image.alpha_composite(frame.convert('RGBA'),glow)
    frame=Image.alpha_composite(frame,overlay)
    d=ImageDraw.Draw(frame)
    for box,color,weight in [(LEFT_CARD,(255,165,130),left_weight),(RIGHT_CARD,(68,255,231),right_weight)]:
        if weight>.01:
            d.rounded_rectangle(box,radius=27,outline=(*color,round(235*weight)),width=5)
    return frame.convert('RGB')


def render(source, output):
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pixel_format','rgb24','-video_size',f'{WIDTH}x{HEIGHT}',
         '-framerate',str(FPS),'-i','pipe:0','-an','-c:v','libx264',
         '-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',
         '-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(NFRAMES):
            proc.stdin.write(render_frame(source,i).tobytes())
        proc.stdin.close()
        err=proc.stderr.read()
        if proc.wait(): raise RuntimeError(err.decode(errors='replace'))
    finally:
        if proc.poll() is None:proc.kill()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--config',required=True)
    p.add_argument('--source-video',help='Local review media ONLY. Never commit.')
    p.add_argument('--synthetic',action='store_true')
    p.add_argument('--output',required=True)
    args=p.parse_args()
    validate(json.loads(Path(args.config).read_text(encoding='utf-8')))
    if bool(args.source_video)==bool(args.synthetic):
        p.error('choose exactly one: --source-video or --synthetic')
    source=synthetic_source() if args.synthetic else extract_first_frame(args.source_video)
    render(source,args.output)

if __name__=='__main__': main()
