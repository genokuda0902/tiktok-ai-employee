"""Three-track audio mixer; accepts only files with explicit source/rights metadata."""
import json
import subprocess
from pathlib import Path

def mix(voice, bgm, sfx, out, duration, rights):
    for role,path in (('VOICE',voice),('BGM',bgm),('SFX',sfx)):
        if not Path(path).is_file() or not rights.get(role,{}).get('source') or not rights[role].get('rights_status'):
            raise ValueError(f'{role} missing source or rights status')
    if duration<=0 or duration>60: raise ValueError('Invalid duration')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    # Explicit ducking keeps background tracks below narration. This does not
    # replace a human listening test, loudness analysis or rights approval.
    graph='[0:a]volume=1.0[v];[1:a]volume=0.08,atrim=duration={d}[b];[2:a]volume=0.12,atrim=duration={d}[s];[v][b][s]amix=inputs=3:duration=first:dropout_transition=0,aresample=48000[m]'.format(d=duration)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(voice),'-stream_loop','-1','-i',str(bgm),'-i',str(sfx),'-filter_complex',graph,'-map','[m]','-c:a','pcm_s16le',str(out)],check=True)
    data={'tracks':{'VOICE':str(voice),'BGM':str(bgm),'SFX':str(sfx)},'rights':rights,'levels':{'VOICE':1.0,'BGM':0.08,'SFX':0.12},'approval':'HUMAN_REVIEW'}
    out.with_suffix('.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    return data
