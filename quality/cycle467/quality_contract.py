"""Genre-neutral fail-closed quality contract for 9:16 review videos."""
import json
from pathlib import Path

REQUIRED = {"asset_rights":"ORIGINAL_SYNTHETIC", "privacy":"NO_REAL_PERSONAL_DATA",
            "quality_status":"HUMAN_REVIEW", "publication":"NOT_APPROVED",
            "auto_post":False, "human_approval":False, "reference_equivalence":False}
SAFE_RECT=(35,160,685,1125)

def validate(plan):
    for k,v in REQUIRED.items():
        if plan.get(k)!=v: raise ValueError(f"unsafe {k}: {plan.get(k)!r}")
    if plan.get("duration")!=20: raise ValueError("unexpected duration")
    scenes=plan.get('scenes',[])
    if not 6<=len(scenes)<=10: raise ValueError("scene count")
    pos=0
    for i,s in enumerate(scenes):
        if abs(s['start']-pos)>1e-6 or s['end']<=s['start']: raise ValueError(f"timeline gap/overlap at {i}")
        if not all(s.get(k) for k in ('title','caption','narration','stage','visual')): raise ValueError(f"empty field at {i}")
        if len(s['caption'])>28: raise ValueError(f"caption too long at {i}")
        pos=s['end']
    if abs(pos-plan['duration'])>1e-6: raise ValueError('duration mismatch')
    if scenes[0]['end']>1.5: raise ValueError('hook too late')
    return True

def caption_safe(rect, w=720,h=1280):
    x1,y1,x2,y2=rect
    return 35<=x1<x2<=685 and 160<=y1<y2<=1125

def validate_narration(plan,manifest):
    """Machine QA: per-scene audio present and within scene bounds. NOT linguistic human QA."""
    if manifest.get('language')!='ja' or manifest.get('engine') not in ('open_jtalk','aivis'):
        raise ValueError('narration source not verified')
    items=manifest.get('segments',[])
    if len(items)!=len(plan['scenes']): raise ValueError('segment count mismatch')
    for s,a in zip(plan['scenes'],items):
        if a.get('text')!=s['narration']: raise ValueError('speech text mismatch')
        if abs(a.get('start',-1)-s['start'])>.03: raise ValueError('speech start mismatch')
        if a.get('duration',0)<=.1 or a['duration']>(s['end']-s['start'])+.03:
            raise ValueError('speech duration mismatch')
    return True

if __name__=='__main__':
    validate(json.loads(Path(__file__).with_name('scene_plan.json').read_text(encoding='utf-8')))
