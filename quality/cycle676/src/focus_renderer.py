"""Review-only, 10-genre reusable focal-region overlay for existing approved MP4s.
No downloads, publishing, or private asset commits.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
from pathlib import Path

def validate_cues(cues, width=1080, height=1920, duration=20):
    if not isinstance(cues, list) or not cues:
        raise ValueError('at least one focus cue required')
    for cue in cues:
        if set(cue) != {'start', 'end', 'x', 'y', 'w', 'h', 'color'}:
            raise ValueError('focus cue schema mismatch')
        s, e = float(cue['start']), float(cue['end'])
        x, y, w, h = [int(cue[k]) for k in ('x','y','w','h')]
        if not (0 <= s < e <= duration):
            raise ValueError('invalid cue timing')
        if not (0 <= x < width and 0 <= y < height and w >= 8 and h >= 8 and x+w <= width and y+h <= height):
            raise ValueError('focus region outside video')
        if cue['color'] not in {'yellow','cyan','green'}:
            raise ValueError('color must be allowlisted')
    ordered=sorted(cues,key=lambda x:x['start'])
    for a,b in zip(ordered,ordered[1:]):
        if float(a['end']) > float(b['start']):
            raise ValueError('overlapping focus cues')
    return True

def make_filter(cues):
    palette={'yellow':'0xFFE16B','cyan':'0x5EE8FF','green':'0x51E8BC'}
    parts=[]
    for c in cues:
        start,end=float(c['start']),float(c['end'])
        x,y,w,h=[int(c[k]) for k in ('x','y','w','h')]
        color=palette[c['color']]
        enabled=f'between(t,{start:.3f},{end:.3f})'
        parts += [
            f"drawbox=x={x-4}:y={y-4}:w={w+8}:h={h+8}:color={color}@0.30:t=16:enable='{enabled}'",
            f"drawbox=x={x}:y={y}:w={w}:h={h}:color={color}@0.98:t=7:enable='{enabled}'",
        ]
    return ','.join(parts)

def render(source:Path, target:Path, cues:list):
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('ffmpeg and ffprobe required')
    if not source.is_file():
        raise FileNotFoundError(source)
    meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)],text=True))
    video=next(s for s in meta['streams'] if s['codec_type']=='video')
    width,height=int(video['width']),int(video['height'])
    duration=float(meta['format']['duration'])
    validate_cues(cues,width,height,duration)
    target.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-y','-i',str(source),'-vf',make_filter(cues),'-map','0:v:0','-map','0:a:0?',
         '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    return target

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--cues',required=True,type=Path)
    args=p.parse_args()
    cfg=json.loads(args.cues.read_text(encoding='utf8'))
    render(args.input,args.output,cfg['cues'])

if __name__=='__main__':main()
