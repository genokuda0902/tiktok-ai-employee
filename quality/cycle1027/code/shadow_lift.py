#!/usr/bin/env python3
"""Review-only shadow-detail lift for 10-genre Japanese vertical slides.

Changes y=150..1389 only. Preserves upper status and lower burned subtitles.
No external media, uploading, paid services, merging, or posting.
"""
import argparse
import subprocess
from pathlib import Path

GENRES = ('ai_work','trivia','cooking','beauty','money','health','travel','product','story','work_skills')
PRESETS = {g: {'shadow':0.23,'midtone':0.55} for g in GENRES}

def filtergraph(genre):
    if genre not in PRESETS:
        raise ValueError(f'Unknown genre: {genre}')
    p=PRESETS[genre]
    curve=f"0/0 0.15/{p['shadow']} 0.5/{p['midtone']} 0.85/0.85 1/1"
    return ("[0:v]split=2[base][roi];"
            f"[roi]crop=1080:1240:0:150,curves=all='{curve}'[lifted];"
            "[base][lifted]overlay=0:150:shortest=1,format=yuv420p[v]")

def render(src,dest,genre='ai_work',preset='veryfast'):
    if not Path(src).is_file():
        raise FileNotFoundError(src)
    Path(dest).parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',src,
         '-filter_complex',filtergraph(genre),'-map','[v]','-map','0:a:0',
         '-map','0:d?','-map_metadata','0','-map_chapters','0',
         '-c:v','libx264','-preset',preset,'-crf','18','-pix_fmt','yuv420p',
         '-c:a','copy','-c:d','copy','-movflags','+faststart',dest]
    subprocess.run(cmd,check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('src');p.add_argument('dest')
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--preset',default='veryfast')
    a=p.parse_args()
    render(a.src,a.dest,a.genre,a.preset)
