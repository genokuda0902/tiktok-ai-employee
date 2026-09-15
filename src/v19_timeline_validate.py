#!/usr/bin/env python3
import json, sys
from pathlib import Path
p=json.loads(Path('output/v19_plan.json').read_text())
sc=p['scenes']; errors=[]
if len(sc)!=16: errors.append('scene_count_not_16')
if abs(sum(float(x['duration']) for x in sc)-36)>0.1: errors.append('timeline_not_36s')
if any(float(x['duration'])>4.0 for x in sc): errors.append('scene_too_long')
eng=[x['engine'] for x in sc]
if len(set(eng))<6: errors.append('insufficient_engine_variety')
# No engine may own more than 35% of the full timeline.
from collections import defaultdict
d=defaultdict(float)
for x in sc:d[x['engine']]+=float(x['duration'])
for k,v in d.items():
    if v/36>0.35: errors.append(f'engine_dominates:{k}:{v}')
result={'ok':not errors,'duration':sum(float(x['duration']) for x in sc),'engine_seconds':dict(d),'errors':errors}
Path('output/v19_timeline_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:sys.exit(5)
