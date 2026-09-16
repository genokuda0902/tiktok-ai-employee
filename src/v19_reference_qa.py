#!/usr/bin/env python3
import json,sys,subprocess
from pathlib import Path
OUT=Path('output'); QA=OUT/'qa'; QA.mkdir(parents=True,exist_ok=True)
plan=json.loads((OUT/'v19_plan.json').read_text()); dna=json.loads((OUT/'v19_reference_dna.json').read_text()) if (OUT/'v19_reference_dna.json').exists() else None
video=OUT/'AI時短ラボ_01_v19.mp4'; scenes=plan['scenes']; total=sum(float(s['duration']) for s in scenes)
engines=len(set(s['engine'] for s in scenes)); max_scene=max(float(s['duration']) for s in scenes)
def changes(p,threshold=.22):
    if not p.exists(): return []
    r=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-filter:v',f"select='gt(scene,{threshold})',showinfo",'-f','null','-'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    xs=[]
    for line in r.stderr.splitlines():
        if 'pts_time:' in line:
            try: xs.append(float(line.split('pts_time:')[1].split()[0]))
            except: pass
    return xs
cuts=changes(video); rendered_rate=round(len(cuts)/total*10,2) if total else 0
ref_rate=float(dna.get('reference_visual_changes_per_10s',0)) if dna else 0
# Scene detector is conservative; require at least 45% of reference hard-cut rate, while planned scene density carries the rest.
cadence_ok=(not dna) or rendered_rate>=max(1.5,ref_rate*0.45)
roles=[s.get('role') for s in scenes]; proof_ids=[s['id'] for s in scenes if s['type'] in {'browser_proof','spreadsheet_proof'}]
report={'reference_mode':bool(dna),'duration':total,'scene_count':len(scenes),'engine_count':engines,'max_scene_duration':max_scene,'rendered_visual_changes':len(cuts),'rendered_visual_changes_per_10s':rendered_rate,'reference_visual_changes_per_10s':ref_rate,'checks':{'visual_variety':engines>=6,'scene_density':len(scenes)>=12,'no_long_static_scene':max_scene<=4.0,'operation_proof':bool(proof_ids),'proof_before_halfway':bool(proof_ids) and min(proof_ids)<=len(scenes)/2,'human_or_character_anchor':sum(s['type'] in ['human','character','cta'] for s in scenes)>=5,'no_generic_next_preview':'next' not in roles,'rendered_cadence':cadence_ok},'final_multimodal_mp4_inspection_required':True}
report['structural_ready']=all(report['checks'].values())
(QA/'v19_reference_qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not report['structural_ready']: sys.exit(5)
