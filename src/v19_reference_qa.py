#!/usr/bin/env python3
import json,sys
from pathlib import Path
OUT=Path('output')
plan=json.loads((OUT/'v19_plan.json').read_text())
dna=json.loads((OUT/'v19_reference_dna.json').read_text()) if (OUT/'v19_reference_dna.json').exists() else None
scenes=plan['scenes']; total=sum(float(s['duration']) for s in scenes)
engines=len(set(s['engine'] for s in scenes)); max_scene=max(float(s['duration']) for s in scenes)
# Structural proxy gate. Final 投稿判定 still requires inspection of the actual rendered MP4.
report={
 'reference_mode':bool(dna), 'duration':total, 'scene_count':len(scenes), 'engine_count':engines,
 'max_scene_duration':max_scene,
 'checks':{
   'visual_variety':engines>=6,
   'scene_density':len(scenes)>=12,
   'no_long_static_scene':max_scene<=4.0,
   'operation_proof':all(t in {s['type'] for s in scenes} for t in ['browser_proof','spreadsheet_proof']),
   'human_or_character_anchor':any(s['type'] in ['human','character'] for s in scenes),
   'no_generic_next_preview':not any(s.get('role')=='next' for s in scenes)
 },
 'final_human_or_multimodal_mp4_inspection_required':True
}
report['structural_ready']=all(report['checks'].values())
Path('output/qa').mkdir(parents=True,exist_ok=True)
(OUT/'qa'/'v19_reference_qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not report['structural_ready']: sys.exit(5)
