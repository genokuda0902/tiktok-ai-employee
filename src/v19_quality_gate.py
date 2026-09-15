#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path

VIDEO = Path(os.environ.get('V19_VIDEO', 'output/AI時短ラボ_01_v19.mp4'))
REPORT = Path('output/qa/v19_quality.json')
REPORT.parent.mkdir(parents=True, exist_ok=True)


def probe(path):
    cmd=['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]
    return json.loads(subprocess.check_output(cmd, text=True))

report={'video':str(VIDEO),'hard_fail':False,'reasons':[],'checks':{}}
if not VIDEO.exists() or VIDEO.stat().st_size < 500_000:
    report['hard_fail']=True; report['reasons'].append('missing_or_tiny_video')
else:
    p=probe(VIDEO)
    vs=next((s for s in p.get('streams',[]) if s.get('codec_type')=='video'),{})
    aud=any(s.get('codec_type')=='audio' for s in p.get('streams',[]))
    w,h=int(vs.get('width',0)),int(vs.get('height',0))
    dur=float(p.get('format',{}).get('duration',0) or 0)
    report['checks'].update(width=w,height=h,duration=dur,audio=aud,size=VIDEO.stat().st_size)
    if (w,h)!=(1080,1920): report['hard_fail']=True; report['reasons'].append('not_1080x1920')
    if not aud: report['hard_fail']=True; report['reasons'].append('no_audio')
    if not 20 <= dur <= 60: report['hard_fail']=True; report['reasons'].append('bad_duration')

# Structural evidence emitted by the director/compositor. This prevents a technically-valid
# PowerPoint-like render from being accepted as premium.
plan=Path('output/v19_plan.json')
if not plan.exists():
    report['hard_fail']=True; report['reasons'].append('missing_scene_plan')
else:
    data=json.loads(plan.read_text())
    scenes=data.get('scenes',[])
    types={s.get('type') for s in scenes}
    report['checks']['scene_count']=len(scenes)
    report['checks']['scene_types']=sorted(x for x in types if x)
    if len(scenes)<12: report['hard_fail']=True; report['reasons'].append('insufficient_scene_count')
    required={'character','human','browser_proof','spreadsheet_proof','before_after','motion_graphics','cta'}
    missing=sorted(required-types)
    if missing: report['hard_fail']=True; report['reasons'].append('missing_scene_types:'+','.join(missing))

REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
if report['hard_fail']:
    sys.exit(2)
