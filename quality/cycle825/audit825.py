"""Fail-closed source-TTS-script to ASS subtitle parity; not speech recognition.
Voice naturalness and word-level alignment remain human-review gates.
"""
from __future__ import annotations
import argparse,json,re,unicodedata
from pathlib import Path

TAG=re.compile(r'\{[^}]*\}')

def normalize(s):
    return ''.join(c for c in unicodedata.normalize('NFKC',s) if not c.isspace())

def parse_time(s):
    h,m,rest=s.split(':');sec,cs=rest.split('.')
    return int(h)*3600+int(m)*60+int(sec)+int(cs)/100

def caption_rows(ass):
    rows=[]
    for line in ass.splitlines():
        if not line.startswith('Dialogue: 0,'):continue
        fields=line[len('Dialogue: '):].split(',',9)
        if len(fields)!=10:raise ValueError('bad ASS event')
        raw=fields[-1]
        if raw.count(r'\N')!=2:raise ValueError('expected three subtitle lines')
        content=TAG.sub('',raw).replace(r'\N','').replace(r'\h',' ')
        rows.append((parse_time(fields[1]),parse_time(fields[2]),normalize(content)))
    return rows

def audit(root:Path)->dict:
    timing=json.loads((root/'source/voice_timing.json').read_text(encoding='utf-8'))
    scenes=timing['sentences']
    rows=caption_rows((root/'output/captions817.ass').read_text(encoding='utf-8'))
    if len(scenes)!=8 or len(rows)!=24:raise ValueError('8 scenes / 24 caption states required')
    t=0.0;checks=[]
    for i,scene in enumerate(scenes):
        start=t;t+=float(scene['seconds'])
        subset=rows[i*3:(i+1)*3]
        expected=normalize(scene['text'])
        for a,b,content in subset:
            if content!=expected:raise ValueError(f'scene {i+1} TTS text vs caption mismatch')
            if not (start-0.12<=a<b<=t+0.12):
                raise ValueError(f'scene {i+1} subtitle outside narration scene')
        if not all(subset[j][1]<=subset[j+1][0]+0.04 for j in range(2)):
            raise ValueError(f'scene {i+1} caption overlap')
        checks.append({'scene':i+1,'source_text_equals_all_3_captions':True,'scene_timing_bounds':True})
    return {'scenes':8,'caption_states':24,'source_text_parity':True,
            'scene_timing_bounds':True,'word_level_audio_alignment_verified':False,
            'human_listening_verified':False,'publication_approved':False,'checks':checks}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();r=audit(a.root);a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False))
