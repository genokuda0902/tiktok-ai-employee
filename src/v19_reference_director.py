#!/usr/bin/env python3
"""Reference-to-Video Director.
Extracts editing DNA from one or more reference MP4s without copying identity/content.
Usage: python3 src/v19_reference_director.py refs/*.mp4
"""
from pathlib import Path
import subprocess,json,sys,statistics

def probe(p):
    raw=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-show_entries','stream=width,height,r_frame_rate','-of','json',str(p)],text=True)
    j=json.loads(raw); v=next(x for x in j['streams'] if 'width' in x)
    return {'file':str(p),'duration':float(j['format']['duration']),'width':v['width'],'height':v['height'],'fps':v['r_frame_rate']}

def scene_changes(p,threshold=.30):
    cmd=['ffmpeg','-hide_banner','-i',str(p),'-filter:v',f"select='gt(scene,{threshold})',showinfo",'-f','null','-']
    r=subprocess.run(cmd,text=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    times=[]
    for line in r.stderr.splitlines():
        if 'pts_time:' in line:
            try: times.append(float(line.split('pts_time:')[1].split()[0]))
            except: pass
    return times

refs=[Path(x) for x in sys.argv[1:] if Path(x).exists()]
if not refs: raise SystemExit('reference MP4 required')
items=[]
for p in refs:
    q=probe(p); cuts=scene_changes(p); q['detected_visual_changes']=cuts
    q['visual_changes_per_10s']=round(len(cuts)/q['duration']*10,2); items.append(q)
median_d=statistics.median(x['duration'] for x in items)
median_change=statistics.median(x['visual_changes_per_10s'] for x in items)
# DNA is structural only; never copy creator identity, wording, logos, or protected footage.
dna={
 'version':'v19-reference-dna-1', 'references':items,
 'reference_median_duration':round(median_d,2),
 'reference_visual_changes_per_10s':round(median_change,2),
 'transfer':['hook intensity','visual-change cadence','presenter-anchor rhythm','proof insertion timing','caption density','return-to-anchor pattern','CTA placement'],
 'never_transfer':['creator identity','exact script','logos','watermarks','reference footage','distinctive protected character'],
 'director_rules':[
   'Use protagonist/brand character as recurring anchor, not a static slideshow host.',
   'Insert real or realistic tool proof as evidence, not decorative UI.',
   'Every scene must introduce visual information, emotion, proof, or payoff.',
   'Duration is content-dependent; do not force 30 seconds when the reference grammar needs more room.',
   'No generic next-episode preview. Series teaser only when a concrete next-part payoff exists.',
   'Reference DNA is a quality target, not a copy instruction.'
 ]
}
out=Path('output'); out.mkdir(exist_ok=True)
(out/'v19_reference_dna.json').write_text(json.dumps(dna,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dna,ensure_ascii=False,indent=2))
