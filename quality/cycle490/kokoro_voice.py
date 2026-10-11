"""Attempt new free Japanese Kokoro narration. Never silently reuse unknown audio."""
import json, numpy as np, soundfile as sf
from pathlib import Path
from kokoro import KPipeline
from render import ENDS,NARRATION
SR=24000
def main():
    out=Path('output/cycle490');out.mkdir(parents=True,exist_ok=True)
    p=KPipeline(lang_code='j')
    track=np.zeros(20*SR,dtype=np.float32);report=[]
    for i,s in enumerate(NARRATION):
        maximum=ENDS[i+1]-ENDS[i]-.3
        selected=None
        for speed in [1.1,1.25,1.4,1.6]:
            chunks=[np.asarray(a,dtype=np.float32) for _,_,a in p(s,voice='jm_kumo',speed=speed)]
            if not chunks:continue
            audio=np.concatenate(chunks);duration=len(audio)/SR
            if duration<=maximum:
                selected=(audio,speed,duration);break
        if selected is None:raise RuntimeError(f'scene {i}: Japanese speech exceeds time window; fail closed')
        audio,speed,duration=selected;start=int((ENDS[i]+.12)*SR)
        track[start:start+len(audio)]+=audio
        report.append({'scene':i,'text':s,'start':ENDS[i]+.12,'duration':duration,'speed':speed})
    sf.write(out/'narration.wav',np.clip(track,-1,1),SR)
    (out/'voice_manifest.json').write_text(json.dumps({'script':NARRATION,'scene_ends':ENDS,'measured_segments_fit':True,'segments':report},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
