#!/usr/bin/env python3
"""v20 zero-cost motion renderer: turns portrait hero images into fast motion clips.
No video-generation API/GPU required. FFmpeg only.
"""
from pathlib import Path
import subprocess, json

ROOT=Path(__file__).resolve().parents[1]
HERO=ROOT/'assets/v19/heroes'
OUT=ROOT/'output/v20_motion'
OUT.mkdir(parents=True,exist_ok=True)

# Fast cuts; deliberately avoid the old multi-second static zoom look.
shots=[
 ('01_robot_hook',1.10,'push'),('02_stressed_worker',1.20,'panr'),
 ('03_robot_solution',1.10,'push'),('09_before_after',1.00,'panl'),
 ('11_robot_cta',1.00,'push'),('12_freedom',1.25,'pull'),
]

def find_asset(stem):
    for ext in ('.png','.jpg','.jpeg','.webp'):
        p=HERO/(stem+ext)
        if p.exists(): return p
    return None

def vf(mode,dur):
    fps=30; frames=max(1,int(dur*fps))
    # overscan then animate crop/scale to create real editorial motion from stills
    base='scale=1200:2134:force_original_aspect_ratio=increase,crop=1200:2134'
    if mode=='push':
        z=f"zoompan=z='min(zoom+0.0028,1.14)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps}"
    elif mode=='pull':
        z=f"zoompan=z='if(eq(on,1),1.14,max(1.0,zoom-0.0028))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps}"
    elif mode=='panr':
        z=f"zoompan=z=1.10:x='min((iw-iw/zoom)*on/{frames},iw-iw/zoom)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps}"
    else:
        z=f"zoompan=z=1.10:x='max((iw-iw/zoom)*(1-on/{frames}),0)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps}"
    return base+','+z+',format=yuv420p'

clips=[]; missing=[]
for i,(stem,dur,mode) in enumerate(shots,1):
    src=find_asset(stem)
    if not src:
        missing.append(stem); continue
    dst=OUT/f'{i:02d}_{stem}.mp4'
    subprocess.run(['ffmpeg','-y','-loop','1','-i',str(src),'-vf',vf(mode,dur),'-t',str(dur),'-r','30','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(dst)],check=True)
    clips.append(dst)

report={'mode':'ZERO_COST_MOTION','gpu_required':False,'paid_video_api_required':False,'clips':[str(x.relative_to(ROOT)) for x in clips],'missing_assets':missing}
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
if missing:
    raise SystemExit('Missing hero assets: '+', '.join(missing))
print(json.dumps(report,ensure_ascii=False,indent=2))
