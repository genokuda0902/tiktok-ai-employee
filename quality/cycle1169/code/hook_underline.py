"""Zero-cost reusable first-second hook underline for portrait narrated slides.

Only the title-divider region is changed. The Japanese narration and subtitle
pixels are not deliberately altered. This is a visual hook, not ASR or a
proven retention uplift. Source MP4 is never uploaded to public CI.
"""
from __future__ import annotations
import argparse
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

FPS = 30
TOTAL_FRAMES = 675
INTRO_FRAMES = 42
ROI = (75, 380, 540, 18)  # x, y, width, height; below opening headline
COLORS = {
    'ai-work': (244, 203, 126), 'finance': (245, 202, 114),
    'career': (142, 222, 163), 'health': (111, 218, 187),
    'learning': (139, 188, 247), 'travel': (244, 167, 126),
    'technology': (126, 175, 250), 'business': (105, 222, 210),
    'life': (230, 159, 206), 'history': (230, 194, 134),
}

def opacity_and_progress(frame: int, count: int = INTRO_FRAMES):
    if not isinstance(frame, int) or not 0 <= frame < count:
        raise ValueError('frame must be inside intro')
    # 0..3 delay; 4..21 draw; 22..29 hold; 30..41 fade
    if frame < 4:
        return 0.0, 0.0
    if frame <= 21:
        u=(frame-3)/18.0
        return min(1.0, u), 0.88
    if frame <= 29:
        return 1.0, 0.88
    return 1.0, 0.88 * max(0.0, (41-frame)/12.0)

def validate(roi=ROI, colors=COLORS, fps=FPS, count=INTRO_FRAMES):
    x,y,w,h=roi
    if not (0<=x<1080 and 0<=y<1920 and w>0 and h>0 and x+w<=1080 and y+h<=1920):
        raise ValueError('Invalid ROI')
    if not (365<=y and y+h<=405):
        raise ValueError('Hook effect must stay in opening headline divider safe strip')
    if len(colors)!=10 or any(len(c)!=3 or any(not 0<=v<=255 for v in c) for c in colors.values()):
        raise ValueError('Exactly 10 valid RGB genre palettes required')
    if fps!=30 or not (1<=count<=45):
        raise ValueError('Invalid frame settings')
    return True

def draw_frame(frame:int, genre='ai-work', size=None):
    validate()
    if genre not in COLORS:
        raise ValueError('Unsupported genre')
    w,h=size or ROI[2:]
    progress, alpha=opacity_and_progress(frame)
    img=Image.new('RGBA',(w,h),(0,0,0,0))
    if progress<=0 or alpha<=0:
        return img
    # A warm underline with a diffuse glow, not a flashing/strobing effect.
    length=int(round((w-12)*progress))
    c=COLORS[genre]
    glow=Image.new('RGBA',(w,h),(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    gd.rounded_rectangle((6,6,6+length,11),radius=2,fill=(*c,int(120*alpha)))
    glow=glow.filter(ImageFilter.GaussianBlur(radius=3))
    img=Image.alpha_composite(img,glow)
    d=ImageDraw.Draw(img)
    d.rounded_rectangle((6,7,6+length,9),radius=1,fill=(*c,int(220*alpha)))
    # Small tip, fading with the underline, gives directional movement.
    if length>=6:
        d.ellipse((4+length,5,10+length,11),fill=(*c,int(110*alpha)))
    return img

def overlays(folder, genre='ai-work'):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=True)
    for f in range(INTRO_FRAMES):
        draw_frame(f,genre).save(folder/f'hook_{f:04d}.png',compress_level=1)
    return INTRO_FRAMES

def probe(path):
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))
    v=next(s for s in data['streams'] if s['codec_type']=='video')
    a=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
    if (v['width'],v['height'])!=(1080,1920) or v.get('avg_frame_rate')!='30/1':
        raise ValueError('Expected 1080x1920 30fps source')
    if a is None or a.get('codec_name')!='aac':
        raise ValueError('Expected AAC Japanese narration source')
    return v,a

def render(source,output,workdir,genre='ai-work',preset='veryfast'):
    source,output,workdir=map(Path,(source,output,workdir))
    probe(source)
    overlays(workdir/'hook_frames',genre)
    output.parent.mkdir(parents=True,exist_ok=True)
    x,y,_,_=ROI
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate',str(FPS),'-i',str(workdir/'hook_frames'/'hook_%04d.png'),
         '-filter_complex',f'[0:v][1:v]overlay={x}:{y}:shortest=0:eof_action=pass:format=auto,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-map_metadata','0',
         '-c:v','libx264','-preset',preset,'-crf','18','-pix_fmt','yuv420p',
         '-c:a','copy','-frames:v',str(TOTAL_FRAMES),'-t',str(TOTAL_FRAMES/FPS),
         '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'change':'intro_hook_underline','genre':genre,'frames':TOTAL_FRAMES,'intro_frames':INTRO_FRAMES,
            'roi':list(ROI),'genre_presets':len(COLORS),'audio_stream_copy':True,
            'asr_semantics_verified':False,'retention_improvement_proven':False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True);p.add_argument('--output',required=True)
    p.add_argument('--workdir',required=True)
    p.add_argument('--genre',default='ai-work',choices=tuple(COLORS))
    p.add_argument('--preset',default='veryfast')
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output,a.workdir,a.genre,a.preset),ensure_ascii=False))
if __name__=='__main__': main()
