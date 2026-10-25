"""Review-only insertion of a locally recorded, sanitized spreadsheet demo.

Preserves the original Japanese AAC track, title, CTA and burned-in subtitles.
Requires local rights approval before publishing any footage. No network,
paid services, auto-posting, or approval bypass.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cycle833.focal_layout import GENRES, FRAMES

FPS=30
W,H=1080,1920
PHOTO_RECT=(62,390,1018,1390)
CTA_TOP=1400
CAPTION_TOP=1452

def frame_window(scene:int):
    if not 0 <= scene < len(FRAMES): raise ValueError('invalid scene index')
    start=sum(FRAMES[:scene])
    return start,start+FRAMES[scene]

def validate(genre:str,scene:int,box=PHOTO_RECT):
    if genre not in GENRES: raise ValueError('unknown genre')
    start,end=frame_window(scene)
    l,t,r,b=box
    if not (0 <= l < r <= W and 0 <= t < b < CTA_TOP and b < CAPTION_TOP):
        raise ValueError('recording overlaps protected caption or CTA zone')
    return start,end

def command(source:Path,clip:Path,out:Path,genre='ai_work',scene=2,font=None):
    start,end=validate(genre,scene)
    source,clip,out=map(Path,(source,clip,out))
    for p in (source,clip):
        if not p.is_file(): raise FileNotFoundError(str(p))
    if out.resolve() in (source.resolve(),clip.resolve()):
        raise ValueError('must not overwrite inputs')
    l,t,r,b=PHOTO_RECT
    pw,ph=r-l,b-t
    begin=start/FPS
    duration=(end-start)/FPS
    font=font or '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    # Crop only Xvfb black margins. Letterbox preserves all spreadsheet columns.
    vf=(f"[1:v]trim=start=0.3:duration={duration:.6f},setpts=PTS-STARTPTS,"
        f"crop=1250:718:58:25,scale={pw-36}:530:flags=lanczos,"
        f"pad={pw}:{ph}:18:235:color=0x0c2734,"
        f"drawbox=x=14:y=229:w={pw-28}:h=542:color=0x36cdbd:t=4,"
        f"drawtext=fontfile={font}:text='実際の表計算操作':fontsize=53:fontcolor=white:x=(w-text_w)/2:y=65,"
        f"drawtext=fontfile={font}:text='架空データでの操作収録・確認用':fontsize=29:fontcolor=0x9de7db:x=(w-text_w)/2:y=826,"
        f"format=rgba,fade=t=in:st=0:d=0.16:alpha=1,"
        f"fade=t=out:st={duration-0.20:.6f}:d=0.20:alpha=1,"
        f"setpts=PTS+{begin:.6f}/TB[demo];"
        f"[0:v][demo]overlay={l}:{t}:eof_action=pass:format=auto,format=yuv420p[v]")
    return ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(clip),
            '-filter_complex',vf,'-map','[v]','-map','0:a:0',
            '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
            '-r',str(FPS),'-c:a','copy','-frames:v',str(sum(FRAMES)),
            '-movflags','+faststart',str(out)]

def render(source,clip,out,genre='ai_work',scene=2,font=None):
    out=Path(out)
    out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(command(Path(source),Path(clip),out,genre,scene,font),check=True)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--clip',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--scene',type=int,default=2)
    p.add_argument('--font')
    a=p.parse_args()
    print(render(a.source,a.clip,a.out,a.genre,a.scene,a.font))
