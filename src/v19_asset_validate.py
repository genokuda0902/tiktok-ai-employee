#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

ROOT=Path('output/v19_assets'); ROOT.mkdir(parents=True,exist_ok=True)
required=['01_robot_hook','02_stressed_worker','03_robot_solution','09_before_after','11_robot_cta','12_device_next','14_city_message']
valid={}; errors=[]
for key in required:
    candidates=[]
    for ext in ('png','jpg','jpeg','webp','mp4','mov','webm'):
        candidates += list(ROOT.glob(f'{key}*.{ext}'))
    if not candidates:
        valid[key]=False; errors.append(f'missing:{key}'); continue
    f=max(candidates,key=lambda p:p.stat().st_size)
    try:
        raw=subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(f)],text=True)
        st=json.loads(raw)['streams'][0]; w,h=int(st['width']),int(st['height'])
        ok=h>w and min(w,h)>=900 and h>=1600
        valid[key]={'ok':ok,'file':str(f),'width':w,'height':h,'bytes':f.stat().st_size}
        if not ok: errors.append(f'low_resolution_or_not_vertical:{key}:{w}x{h}')
    except Exception as e:
        valid[key]=False; errors.append(f'unreadable:{key}:{e}')

ready=not errors
report={'ready':ready,'assets':valid,'errors':errors}
Path('output/v19_assets/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
if ready:
    Path('output/v19_assets/hero_ready.json').write_text(json.dumps({'ready':True,'validated':required},ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
if not ready: sys.exit(4)
