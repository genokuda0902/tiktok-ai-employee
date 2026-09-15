#!/usr/bin/env python3
import json, sys
from pathlib import Path
plan=Path('output/v19_plan.json'); manifest=Path('output/v19_asset_manifest.json')
checks={
 'plan':plan.exists(),
 'asset_manifest':manifest.exists(),
 'scene_renderer':Path('studio/v19_scene_renderer.mjs').exists(),
 'proof_renderer':Path('studio/v19-proof.mjs').exists(),
 'quality_gate':Path('src/v19_quality_gate.py').exists()
}
if plan.exists():
 p=json.loads(plan.read_text()); checks['sixteen_scenes']=len(p.get('scenes',[]))==16
else: checks['sixteen_scenes']=False
# Premium hero generation is intentionally a hard dependency: do not silently fall back
# to emoji/Pillow/old storyboard crops and call the video finished.
hero=Path('output/v19_assets/hero_ready.json')
checks['premium_hero_assets']=hero.exists()
ready=all(checks.values())
result={'version':'v19','production_ready':ready,'checks':checks,'rule':'Never downgrade missing premium hero assets to PowerPoint-like placeholders.'}
Path('output').mkdir(exist_ok=True); Path('output/v19_preflight.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
if not ready: sys.exit(3)
