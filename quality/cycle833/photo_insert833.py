"""Review-only cinematic photo insert. Source MP4 supplies Japanese voice/captions.
Image and audio rights require separate human approval. No posting or paid API.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse
import subprocess

GENRES = ('sales_business','ai_work','beauty','love_psychology','money_saving',
          'career','health_life','science','travel_food','product_life')
W,H,FPS=1080,1920,30
PHOTO_BOX=(54,390,1026,1210)
CTA_TOP=1240
CAPTION_TOP=1450
HOOK_FRAMES=101

@dataclass(frozen=True)
class PhotoInsert:
    genre: str='ai_work'
    start_frame: int=0
    end_frame: int=HOOK_FRAMES
    box: tuple[int,int,int,int]=PHOTO_BOX
    def validate(self):
        if self.genre not in GENRES: raise ValueError('unknown genre')
        if not (0<=self.start_frame<self.end_frame<=775): raise ValueError('invalid frame range')
        l,t,r,b=self.box
        if not (0<=l<r<=W and 0<=t<b<CTA_TOP and b<CAPTION_TOP):
            raise ValueError('photo overlaps CTA or Japanese caption safe zone')

def command(base:Path,photo:Path,out:Path,spec:PhotoInsert=PhotoInsert()):
    spec.validate()
    for p in (base,photo):
        if not Path(p).is_file(): raise FileNotFoundError(str(p))
    if Path(out).resolve() in (Path(base).resolve(),Path(photo).resolve()):
        raise ValueError('output must differ from source')
    l,t,r,b=spec.box
    fw,fh=r-l,b-t
    st=spec.start_frame/FPS;en=spec.end_frame/FPS
    fg=(f"[1:v]scale={fw+120}:{fh+260}:force_original_aspect_ratio=increase,"
        f"crop={fw+100}:{fh+80}:x='(in_w-out_w)/2+12*sin(n/17)':"
        f"y='max(0,(in_h-out_h)/2-180)',"
        f"scale={fw}:{fh},format=rgba,"
        f"fade=t=in:st={st:.4f}:d=0.18:alpha=1,"
        f"fade=t=out:st={en-0.23:.4f}:d=0.23:alpha=1[p];"
        f"[0:v][p]overlay={l}:{t}:enable='between(t,{st:.4f},{en-1/FPS:.4f})':"
        f"shortest=1:format=auto,format=yuv420p[v]")
    return ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(base),
            '-loop','1','-framerate',str(FPS),'-i',str(photo),
            '-filter_complex',fg,'-map','[v]','-map','0:a:0',
            '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
            '-r',str(FPS),'-c:a','copy','-movflags','+faststart',
            '-frames:v','775',str(out)]

def render(base,photo,out,genre='ai_work'):
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(command(Path(base),Path(photo),out,PhotoInsert(genre=genre)),check=True)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--base',type=Path,required=True)
    p.add_argument('--photo',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    a=p.parse_args()
    print(render(a.base,a.photo,a.out,a.genre))
