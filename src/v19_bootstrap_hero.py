#!/usr/bin/env python3
"""Stage only validated independent hero assets into output/v19_assets.
This intentionally refuses storyboard collages and generated UI/text posters.
Binary hero masters are committed separately as repository blobs/assets; this script
copies them into runtime names consumed by v19_asset_validate.py.
"""
from pathlib import Path
import json, shutil, sys
SRC=Path('assets/v19/heroes'); DST=Path('output/v19_assets'); DST.mkdir(parents=True,exist_ok=True)
required=['01_robot_hook','02_stressed_worker','03_robot_solution','09_before_after','11_robot_cta','12_device_next','14_city_message']
errors=[]; staged=[]
for key in required:
    found=[]
    for ext in ('png','jpg','jpeg','webp','mp4','mov','webm'):
        found += list(SRC.glob(key+'*.'+ext))
    if not found:
        errors.append('missing_repo_hero:'+key); continue
    src=max(found,key=lambda p:p.stat().st_size)
    dst=DST/src.name; shutil.copy2(src,dst); staged.append(str(dst))
report={'staged':staged,'errors':errors,'ready_for_validation':not errors}
Path('output/v19_hero_bootstrap.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors: sys.exit(6)
