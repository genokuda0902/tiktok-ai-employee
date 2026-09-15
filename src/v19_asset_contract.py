#!/usr/bin/env python3
import json
from pathlib import Path

PLAN=Path('output/v19_plan.json')
OUT=Path('output/v19_asset_manifest.json')
if not PLAN.exists(): raise SystemExit('run v19_scene_plan.py first')
plan=json.loads(PLAN.read_text())

assets=[]
for s in plan['scenes']:
    t=s['type']; sid=s['id']
    if t in {'character','human','before_after','cta'}:
        source='premium_scene_asset'
        requirement='independent vertical hero visual; no storyboard crop; depth; subject separation; camera-motion safe'
    elif t=='browser_proof':
        source='playwright_screencast'
        requirement='realistic animated AI workflow; cursor/action/state changes; full-resolution UI'
    elif t=='spreadsheet_proof':
        source='browser_spreadsheet_motion'
        requirement='animated cells/paste/chart; legible at phone size'
    else:
        source='html_motion_graphics'
        requirement='kinetic typography/icons; no static slide longer than 2.2 seconds'
    assets.append({'scene_id':sid,'type':t,'source':source,'requirement':requirement,'status':'required'})

manifest={
 'version':'v19',
 'policy':{
   'ffmpeg_role':'final compositor only',
   'forbid_old_storyboard_crop':True,
   'forbid_single_proof_loop':True,
   'hero_asset_min_short_edge':900,
   'scene_asset_isolation':True
 },
 'assets':assets
}
OUT.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(manifest,ensure_ascii=False,indent=2))
