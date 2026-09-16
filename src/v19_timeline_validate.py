#!/usr/bin/env python3
import json,sys
from pathlib import Path
from collections import defaultdict
p=json.loads(Path('output/v19_plan.json').read_text()); sc=p['scenes']; errors=[]
total=sum(float(x['duration']) for x in sc)
if len(sc)<12 or len(sc)>24: errors.append('scene_count_out_of_range')
if not 25<=total<=60: errors.append('duration_out_of_range')
if any(float(x['duration'])<=0 or float(x['duration'])>4.0 for x in sc): errors.append('invalid_scene_duration')
eng=[x['engine'] for x in sc]
if len(set(eng))<6: errors.append('insufficient_engine_variety')
d=defaultdict(float)
for x in sc:d[x['engine']]+=float(x['duration'])
for k,v in d.items():
 if v/total>0.40: errors.append(f'engine_dominates:{k}:{v}')
if p.get('reference_mode') and abs(total-float(p['reference_target']['target_duration']))>.15: errors.append('reference_timeline_mismatch')
result={'ok':not errors,'scene_count':len(sc),'duration':total,'engine_seconds':dict(d),'reference_mode':bool(p.get('reference_mode')),'errors':errors}
Path('output/v19_timeline_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:sys.exit(5)
