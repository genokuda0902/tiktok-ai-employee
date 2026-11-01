"""Cycle1161: scene02 sequential focus; synthetic 10-genre accents only.
No private media, speech transcription, or publication approval is included.
"""
from __future__ import annotations
import argparse
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

FPS = 30
START_FRAME = 116
FRAME_COUNT = 49
X, Y, W, H = 95, 620, 920, 570
GENRES = {
    'ai-work':'#4cdbcf', 'finance':'#e1c46c', 'career':'#79d5b4',
    'health':'#81d3c4', 'learning':'#8ac6f3', 'travel':'#f0b77c',
    'technology':'#87bdf0', 'business':'#56ced0', 'life':'#e7acd0',
    'history':'#dfb77d',
}
ROWS = ((23,30,430,148), (23,169,430,288), (23,309,430,428))

def validate():
    assert X >= 0 and Y >= 400 and X+W <= 1080 and Y+H < 1330
    assert START_FRAME >= 100 and START_FRAME+FRAME_COUNT <= 168
    assert all(0<=x0<x1<W and 0<=y0<y1<H for x0,y0,x1,y1 in ROWS)
    return True

def rgba(color,alpha):
    return tuple(bytes.fromhex(color.lstrip('#')))+(int(alpha),)

def ease(t):
    t=max(0.,min(1.,t))
    return t*t*(3-2*t)

def draw_frame(index,genre='ai-work'):
    if not 0<=index<FRAME_COUNT: raise ValueError('Frame outside scene02')
    if genre not in GENRES: raise ValueError('Unknown genre')
    validate()
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(im)
    c=GENRES[genre]
    if index<36:
        active=index//12
        local=(index%12)/11
        alpha=.22+.78*math.sin(math.pi*local)
        x0,y0,x1,y1=ROWS[active]
        for spread,a,width in ((9,26,11),(4,60,7),(0,190,4)):
            d.rounded_rectangle((x0-spread,y0-spread,x1+spread,y1+spread),
                                radius=24+spread,outline=rgba(c,a*alpha),width=width)
        glint_x=int(x0+32+(x1-x0-64)*ease(local))
        d.ellipse((glint_x-6,y0-9,glint_x+6,y0+3),fill=rgba('#e5fffc',180*alpha))
    else:
        progress=ease((index-36)/12)
        for j in range(3):
            t=max(0,min(1,progress-j*.12))
            px=435+int(80*t)
            py=335-int(16*t)
            radius=5-j
            d.ellipse((px-radius,py-radius,px+radius,py+radius),fill=rgba(c,180-j*36))
        a=int(115*math.sin(math.pi*progress))
        if a>0:
            d.ellipse((528,224,562,258),outline=rgba(c,a),width=4)
    return im

def command(args):
    return subprocess.run(args,check=True,capture_output=True,text=True)

def make_overlay(path,genre='ai-work'):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pixel_format','rgba','-video_size',f'{W}x{H}','-framerate',str(FPS),
         '-i','pipe:0','-c:v','qtrle','-pix_fmt','argb',str(path)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(FRAME_COUNT):p.stdin.write(draw_frame(i,genre).tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace')
        if p.wait():raise RuntimeError(err)
    finally:
        if p.poll() is None:p.kill();p.wait()
    return path

def render(source,output,overlay,genre='ai-work',preset='veryfast'):
    source,output=Path(source),Path(output)
    probe=json.loads(command(['ffprobe','-v','error','-show_streams','-of','json',str(source)]).stdout)
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'],v['avg_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('Source must be 1080x1920, 30fps')
    if not any(s['codec_type']=='audio' for s in probe['streams']):
        raise ValueError('Narration audio source required')
    make_overlay(overlay,genre)
    output.parent.mkdir(parents=True,exist_ok=True)
    filt=f'[1:v]setpts=PTS+{START_FRAME/FPS}/TB[ov];[0:v][ov]overlay={X}:{Y}:shortest=0:eof_action=pass:format=auto,format=yuv420p[v]'
    command(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-i',str(overlay),'-filter_complex',filt,'-map','[v]','-map','0:a:0',
             '-map_metadata','0','-c:v','libx264','-crf','18','-preset',preset,
             '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)])
    return {'frames':FRAME_COUNT,'start_frame':START_FRAME,
            'last_frame':START_FRAME+FRAME_COUNT-1,'genres':len(GENRES),
            'audio_stream_copy':True,'independent_asr':False,
            'publication_approved':False,'genre':genre}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--overlay',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai-work')
    p.add_argument('--preset',default='veryfast')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.overlay,a.genre,a.preset),
                     ensure_ascii=False,indent=2))
if __name__=='__main__':main()
