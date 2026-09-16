#!/usr/bin/env python3
"""Apply structural reference DNA to the original v19 plan without copying reference content."""
from pathlib import Path
import json, math
OUT=Path('output')
plan=json.loads((OUT/'v19_plan.json').read_text(encoding='utf-8'))
dna_path=OUT/'v19_reference_dna.json'
if not dna_path.exists():
    print('No reference DNA: keeping native v19 plan')
    raise SystemExit(0)
dna=json.loads(dna_path.read_text(encoding='utf-8'))
ref_dur=float(dna.get('reference_median_duration',sum(float(s['duration']) for s in plan['scenes'])))
ref_rate=float(dna.get('reference_visual_changes_per_10s',4.0))
# Keep topic concise while borrowing reference pacing. Never blindly stretch to reference duration.
target=max(28.0,min(48.0,ref_dur*0.72))
scenes=plan['scenes']
base=sum(float(s['duration']) for s in scenes)
scale=target/base
for s in scenes:
    d=float(s['duration'])*scale
    # Proof/payoff can breathe; hooks/anchors stay fast.
    if s['role'] in {'hook','pain','solution','brand','finale'}: d=min(d,2.25)
    if s['type'] in {'browser_proof','spreadsheet_proof'}: d=max(1.8,min(d,3.0))
    s['duration']=round(d,2)
# cadence contract used by downstream QA/renderers
plan['reference_mode']=True
plan['reference_dna_version']=dna.get('version')
plan['reference_target']={
 'reference_duration':ref_dur,
 'target_duration':round(sum(float(s['duration']) for s in scenes),2),
 'visual_changes_per_10s':ref_rate,
 'max_anchor_gap_seconds':8.0,
 'proof_required_before_halfway':True,
 'copy_reference_content':False
}
plan['director_notes']=['recurring protagonist/robot anchor','real proof as evidence','visual novelty every scene','no fixed next preview']
(OUT/'v19_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'v19_scene_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(plan['reference_target'],ensure_ascii=False,indent=2))
