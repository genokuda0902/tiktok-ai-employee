"""Chapter-synchronized sweep: fixes cycle1135's fixed-interval flash timing.
Only original geometry, no external images, no audio/caption edits.
"""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image

PALETTES = {
    'ai_workflow':'#5ce0d1','business':'#6aaeff',
    'finance':'#e3bf75','health':'#73d6a7',
    'beauty':'#ef9bbd','travel':'#77d4ed',
    'education':'#a79bf4','lifestyle':'#f1ba88',
    'technology':'#8bd5fa','entertainment':'#e59be7',
}

def probe_chapter_cuts(path, fps=30):
    data=json.loads(subprocess.check_output(
        ['ffprobe','-v','error','-show_chapters','-of','json',str(path)],text=True))
    starts=[float(c['start_time']) for c in data.get('chapters',[])]
    cuts=sorted(set(round(round(t*fps)/fps,6) for t in starts if t>0.01))
    if not cuts: raise ValueError('No chapters: provide verified --cuts')
    return cuts

def sweep_x_expr(cuts, duration=.22, width=1080, stripe_width=600):
    if not cuts or duration<=0: raise ValueError('Invalid cuts/duration')
    if any(b-a<=duration for a,b in zip(cuts,cuts[1:])):
        raise ValueError('Overlapping sweep windows')
    speed=(width+stripe_width)/duration
    expr='NAN'
    for cut in reversed(cuts):
        s=f'{cut:.6f}'; e=f'{cut+duration:.6f}'
        expr=f'if(between(t,{s},{e}),-{stripe_width}+(t-{s})*{speed:.5f},{expr})'
    return expr

def sweep_active(t,cuts,duration=.22):
    return any(c<=t<=c+duration for c in cuts)

def make_sweep(path,color,width=600,height=64):
    if color not in PALETTES.values(): raise ValueError('Unknown palette')
    rgb=tuple(int(color[i:i+2],16) for i in (1,3,5))
    im=Image.new('RGBA',(width,height),(0,0,0,0))
    px=im.load()
    for y in range(height):
        fy=max(0,1-abs(y-(height-1)/2)/(height/2))**1.8
        for x in range(width):
            fx=max(0,1-abs(x-(width-1)/2)/(width/2))**1.4
            px[x,y]=(*rgb,round(100*fx*fy))
    im.save(path)
    return im

def render(source,output,genre='ai_workflow',cuts=None,duration=.22):
    source=Path(source); output=Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    cuts=probe_chapter_cuts(source) if cuts is None else list(cuts)
    stripe=output.with_suffix('.sweep.png')
    make_sweep(stripe,PALETTES[genre])
    filt=f"[0:v][1:v]overlay=x='{sweep_x_expr(cuts,duration)}':y=365:eval=frame:shortest=1:format=auto,format=yuv420p[v]"
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-loop','1','-framerate','30','-i',str(stripe),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0',
         '-map_metadata','0','-map_chapters','0',
         '-c:v','libx264','-preset','veryfast','-crf','18',
         '-pix_fmt','yuv420p','-r','30','-threads','4',
         '-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'cuts_seconds':cuts,'output':str(output),'genre':genre,
            'audio':'bitstream copied; semantic Japanese ASR NOT verified'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',choices=PALETTES,default='ai_workflow')
    p.add_argument('--cuts',help='Comma-separated verified scene starts for chapterless synthetic assets')
    a=p.parse_args()
    cuts=[float(x) for x in a.cuts.split(',')] if a.cuts else None
    print(json.dumps(render(a.source,a.output,a.genre,cuts),ensure_ascii=False))
