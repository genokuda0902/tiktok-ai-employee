"""Cycle784: animated circuit connection tracer. Offline Pillow + FFmpeg."""
from __future__ import annotations
import argparse, json, math, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS = 1080, 1360, 30
ROUTE = [(296,713),(379,713),(397,687),(423,739),(449,687),
         (475,739),(501,687),(527,739),(553,687),(575,713),
         (590,713),(690,713),(755,713),(820,713),(940,713),
         (940,787),(940,800),(940,817),(940,834)]
START = 8.10
END = 9.40

def cumulative_lengths(points):
    lengths=[0.0]
    for a,b in zip(points,points[1:]):
        lengths.append(lengths[-1]+math.dist(a,b))
    return lengths

def point_on_path(points, fraction):
    if not 0 <= fraction <= 1: raise ValueError('fraction outside 0..1')
    lengths=cumulative_lengths(points)
    target=lengths[-1]*fraction
    for i in range(1,len(lengths)):
        if target <= lengths[i]:
            k=(target-lengths[i-1])/(lengths[i]-lengths[i-1])
            return tuple(round(points[i-1][j]*(1-k)+points[i][j]*k,2) for j in (0,1))
    return points[-1]

def route_tail(points, fraction, tail_px=95):
    lengths=cumulative_lengths(points)
    target=lengths[-1]*fraction
    back=max(0,target-tail_px)
    sampled=[]
    for length in range(math.floor(back),math.ceil(target)+1,5):
        sampled.append(point_on_path(points,min(1,max(0,length/lengths[-1]))))
    sampled.append(point_on_path(points,fraction))
    return sampled

def make_frame(index, count, accent=(82,235,208)):
    t=index/max(1,count-1)
    fade=max(0,min(1.0,index/4.0,(count-1-index)/4.0))
    fraction=t*t*(3-2*t)
    pos=point_on_path(ROUTE,fraction)
    tail=route_tail(ROUTE,fraction)
    glow=Image.new('RGBA',(W,H),(0,0,0,0))
    gd=ImageDraw.Draw(glow)
    if len(tail)>1:
        gd.line(tail,fill=(*accent,int(110*fade)),width=26,joint='curve')
    x,y=pos
    gd.ellipse((x-34,y-34,x+34,y+34),fill=(*accent,int(175*fade)))
    glow=glow.filter(ImageFilter.GaussianBlur(16))
    sharp=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(sharp)
    if len(tail)>1:
        d.line(tail,fill=(220,255,247,int(135*fade)),width=5,joint='curve')
    d.ellipse((x-10,y-10,x+10,y+10),fill=(245,255,252,int(220*fade)))
    d.ellipse((x-5,y-5,x+5,y+5),fill=(*accent,int(255*fade)))
    return Image.alpha_composite(glow,sharp)

def generate_frames(folder, start=START, end=END, fps=FPS):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    count=round((end-start)*fps)
    for i in range(count):
        make_frame(i,count).save(folder/f'{i:04d}.png',optimize=True)
    return count

def render(source, output, frame_folder, start=START, fps=FPS):
    if not shutil.which('ffmpeg'): raise RuntimeError('ffmpeg not installed')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    filt=f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start:.3f}/TB[fx];[0:v][fx]overlay=x=0:y=0:eof_action=pass:repeatlast=0:format=auto,format=yuv420p[v]'
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),
         '-framerate',str(fps),'-start_number','0','-i',str(Path(frame_folder)/'%04d.png'),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0',
         '-c:v','libx264','-preset','medium','-crf','18','-r',str(fps),
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',
         '-metadata','comment=HUMAN_REVIEW; publication not approved',str(output)]
    subprocess.run(cmd,check=True)
    return output

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--frames',default='output/trace_frames')
    a=p.parse_args()
    n=generate_frames(a.frames)
    render(a.source,a.output,a.frames)
    print(json.dumps({'frames':n,'output':a.output,'status':'HUMAN_REVIEW'},ensure_ascii=False))

if __name__=='__main__':main()
