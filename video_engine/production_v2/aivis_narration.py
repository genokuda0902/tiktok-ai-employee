"""Plan-driven AivisSpeech narration. Voice-model licensing is reviewed separately."""
import io
import json
import os
import urllib.parse
import urllib.request
import wave
from pathlib import Path

def get(url, data=None):
    req=urllib.request.Request(url,data=data,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=40) as r:
        return r.read()

def _scene_id(scene):
    """Canonical identity for AivisSpeech and production renderer."""
    primary = scene.get('scene_id')
    legacy = scene.get('id')
    if primary and legacy and primary != legacy:
        raise RuntimeError('Conflicting scene_id and legacy id')
    sid = primary or legacy
    if not isinstance(sid, str) or not sid.strip():
        raise RuntimeError('Missing scene identity')
    return sid

def _scene_lines(plan):
    lines=[]
    seen=set()
    for scene in plan.get('scenes',[]):
        sid=_scene_id(scene)
        if sid in seen: raise RuntimeError('Duplicate scene identity')
        seen.add(sid)
        narration=(scene.get('narration') or scene.get('message') or '').strip()
        caption=(scene.get('caption') or scene.get('message') or narration).strip()
        if not narration or not caption:
            raise RuntimeError(f"Scene {sid} missing narration/caption source")
        lines.append((scene,narration,caption))
    if not lines:
        raise RuntimeError('Plan has no scenes')
    return lines

def _caption_timeline(chunks):
    """Build deterministic caption timing from measured synthesized scene durations."""
    timeline=[]; cursor=0.0
    for scene,_,seconds,_,caption in chunks:
        if seconds <= 0:
            raise RuntimeError('Caption duration must be positive')
        start=cursor
        end=start+seconds
        timeline.append({
            'scene_id':_scene_id(scene),
            'start':round(start,3),
            'end':round(end,3),
            'text':caption,
        })
        cursor=end
    return timeline

def synthesize(plan_path, base='http://127.0.0.1:10101'):
    path=Path(plan_path).resolve()
    plan=json.loads(path.read_text(encoding='utf8'))
    speakers=json.loads(get(base+'/speakers'))
    name=os.environ.get('AIVIS_SPEAKER_NAME','Flow').lower()
    style=os.environ.get('AIVIS_STYLE_NAME','04_FUN').lower()
    speaker=next((s for s in speakers if name in s['name'].lower()),None)
    if not speaker: raise RuntimeError('Expected Aivis speaker unavailable')
    voice=next((v for v in speaker['styles'] if style in v['name'].lower()),None)
    if not voice: raise RuntimeError('Expected Aivis style unavailable')

    chunks=[]; rate=channels=width=None
    for scene,text,caption in _scene_lines(plan):
        query=json.loads(get(base+'/audio_query?'+urllib.parse.urlencode({'text':text,'speaker':voice['id']}),b''))
        query['speedScale']=1.0
        wav=get(base+'/synthesis?'+urllib.parse.urlencode({'speaker':voice['id']}),json.dumps(query,ensure_ascii=False).encode())
        with wave.open(io.BytesIO(wav),'rb') as audio:
            spec=(audio.getframerate(),audio.getnchannels(),audio.getsampwidth())
            if rate is None: rate,channels,width=spec
            if spec!=(rate,channels,width): raise RuntimeError('Changing WAV format')
            frames=audio.readframes(audio.getnframes())
            seconds=audio.getnframes()/rate
        if seconds < 0.45 or seconds > 5.0:
            raise RuntimeError(f'Unnatural segment duration {seconds:.2f}; review scene wording')
        chunks.append((scene,frames,seconds,text,caption))

    total=sum(item[2] for item in chunks)
    if not 15 <= total <= 25:
        raise RuntimeError(f'Unexpected real speech duration {total:.2f}; edit plan wording rather than stretching audio')

    out=path.parent/'narration_jp.wav'
    with wave.open(str(out),'wb') as audio:
        audio.setnchannels(channels); audio.setsampwidth(width); audio.setframerate(rate)
        for _,frames,_,_,_ in chunks: audio.writeframes(frames)

    for scene,_,seconds,text,caption in chunks:
        scene.update(duration=seconds,narration=text,caption=caption)

    caption_timeline=_caption_timeline(chunks)
    plan.update(
        narration_file=out.name,
        narration=''.join(x[3] for x in chunks),
        captions=' / '.join(x[4] for x in chunks),
        caption_timeline=caption_timeline,
        caption_timing_source='measured_aivis_scene_duration',
        expected_seconds=total,
        voice_metadata={
            'engine':'AivisSpeech','speaker':speaker['name'],'style':voice['name'],
            'model_commercial_rights':'UNVERIFIED',
            'human_pronunciation_review':'PENDING',
            'semantic_source':'plan.scenes'
        }
    )
    path.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'narration_file':str(out),'measured_duration':total,'rights':'UNVERIFIED','approval':'NOT_APPROVED'}))

if __name__=='__main__':
    import sys
    synthesize(sys.argv[1])
