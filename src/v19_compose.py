#!/usr/bin/env python3
import json, subprocess, shlex
from pathlib import Path

OUT=Path('output'); AS=OUT/'v19_assets'; SC=OUT/'v19_scenes'; TMP=OUT/'v19_clips'
TMP.mkdir(parents=True,exist_ok=True)
plan=json.loads((OUT/'v19_plan.json').read_text())
hero_map={1:'01_robot_hook',2:'02_stressed_worker',3:'03_robot_solution',9:'09_before_after',11:'11_robot_cta',12:'12_device_next',13:'11_robot_cta',14:'14_city_message',16:'11_robot_cta'}

def pick(prefix):
    for ext in ('mp4','mov','webm','png','jpg','jpeg','webp'):
        fs=sorted(AS.glob(prefix+'*.'+ext))
        if fs:return fs[0]
    return None

def run(cmd):
    print('+',' '.join(shlex.quote(str(x)) for x in cmd)); subprocess.check_call([str(x) for x in cmd])

clips=[]
for s in plan['scenes']:
    i=s['id']; dur=float(s['duration']); clip=TMP/f'{i:02d}.mp4'
    src=pick(hero_map[i]) if i in hero_map else None
    if src is None:
        # proof/motion scenes are generated independently by browser renderers
        candidates=[SC/f'scene_{i:02d}.mp4',SC/f'scene_{i:02d}.webm',SC/f'scene_{i:02d}.png']
        src=next((p for p in candidates if p.exists()),None)
    if src is None: raise SystemExit(f'missing independent scene source {i}')
    if src.suffix.lower() in {'.png','.jpg','.jpeg','.webp'}:
        # cinematic Ken Burns motion on a high-res independent master, never a collage crop
        vf=f"scale=1240:2205:force_original_aspect_ratio=increase,crop=1080:1920:x='(iw-ow)/2+18*sin(t*1.7)':y='(ih-oh)/2+12*cos(t*1.3)',zoompan=z='min(zoom+0.0008,1.08)':d=1:s=1080x1920:fps=30,format=yuv420p"
        run(['ffmpeg','-y','-loop','1','-i',src,'-t',str(dur),'-vf',vf,'-an','-c:v','libx264','-preset','medium','-crf','15',clip])
    else:
        vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p"
        run(['ffmpeg','-y','-i',src,'-t',str(dur),'-vf',vf,'-an','-c:v','libx264','-preset','medium','-crf','15',clip])
    clips.append(clip)

lst=TMP/'concat.txt'; lst.write_text('\n'.join("file '"+str(p.resolve()).replace("'","'\\''")+"'" for p in clips))
visual=OUT/'v19_visual.mp4'
run(['ffmpeg','-y','-f','concat','-safe','0','-i',lst,'-c:v','libx264','-preset','medium','-crf','15','-pix_fmt','yuv420p',visual])
voice=OUT/'narration.wav'
final=OUT/'AI時短ラボ_01_v19.mp4'
if not voice.exists(): raise SystemExit('missing narration.wav')
run(['ffmpeg','-y','-i',visual,'-i',voice,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',final])
print(final)
