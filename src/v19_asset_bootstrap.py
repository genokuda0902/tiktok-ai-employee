#!/usr/bin/env python3
from pathlib import Path
import shutil, json, sys
SRC=Path('assets/v19/heroes'); DST=Path('output/v19_assets'); DST.mkdir(parents=True,exist_ok=True)
required=['01_robot_hook','02_stressed_worker','03_robot_solution','09_before_after','11_robot_cta','12_freedom']
exts=['.png','.jpg','.jpeg','.webp','.mp4','.mov','.webm']
copied={}; missing=[]
for stem in required:
    found=next((SRC/f'{stem}{ext}' for ext in exts if (SRC/f'{stem}{ext}').exists()),None)
    if not found: missing.append(stem); continue
    target=DST/found.name; shutil.copy2(found,target); copied[stem]=str(target)
report={'source':str(SRC),'destination':str(DST),'required':required,'copied':copied,'missing':missing}
(DST/'bootstrap.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if missing:
    print('Premium hero source assets missing; placeholders are forbidden.',file=sys.stderr)
    raise SystemExit(4)
