"""AivisSpeech technical narration on a trusted runner. Voice-model licensing is separate."""
import io
import json
import os
import urllib.parse
import urllib.request
import wave
from pathlib import Path

LINES = [
 ('この山積みの作業、まだ手入力ですか？','まだ手入力？'),
 ('必要な情報を、短くまとめます。','情報を絞る'),
 ('まず、項目を確認して。','項目を確認'),
 ('エーアイに、整理する条件を伝えます。','条件を伝える'),
 ('出力を、ひとつずつ確かめます。','一つずつ確認'),
 ('そのまま使わず、誤りを直します。','誤りを修正'),
 ('最後に、人が判断します。','判断は人がする'),
 ('この流れ、保存して試してください。','保存して試す'),
]

def get(url,data=None):
    with urllib.request.urlopen(urllib.request.Request(url,data=data,headers={'Content-Type':'application/json'}),timeout=40) as r:return r.read()

def synthesize(plan_path, base='http://127.0.0.1:10101'):
    path=Path(plan_path).resolve();plan=json.loads(path.read_text(encoding='utf8'))
    speakers=json.loads(get(base+'/speakers'))
    name=os.environ.get('AIVIS_SPEAKER_NAME','Flow').lower()
    style=os.environ.get('AIVIS_STYLE_NAME','04_FUN').lower()
    speaker=next((s for s in speakers if name in s['name'].lower()),None)
    if not speaker:raise RuntimeError('Expected Aivis speaker unavailable')
    voice=next((v for v in speaker['styles'] if style in v['name'].lower()),None)
    if not voice:raise RuntimeError('Expected Aivis style unavailable')
    chunks=[];rate=None;channels=None;width=None
    for text,caption in LINES:
        query=json.loads(get(base+'/audio_query?'+urllib.parse.urlencode({'text':text,'speaker':voice['id']}),b''))
        query['speedScale']=1.0
        wav=get(base+'/synthesis?'+urllib.parse.urlencode({'speaker':voice['id']}),json.dumps(query,ensure_ascii=False).encode())
        with wave.open(io.BytesIO(wav),'rb') as audio:
            spec=(audio.getframerate(),audio.getnchannels(),audio.getsampwidth())
            if rate is None:rate,channels,width=spec
            if spec!=(rate,channels,width):raise RuntimeError('Changing WAV format')
            frames=audio.readframes(audio.getnframes());seconds=audio.getnframes()/rate
        if seconds<1.0 or seconds>5.0:raise RuntimeError('Unnatural segment duration; review script')
        chunks.append((frames,seconds,text,caption))
    total=sum(item[1] for item in chunks)
    if not 15<=total<=25:raise RuntimeError(f'Unexpected real speech duration {total:.2f}; edit wording rather than stretching audio')
    out=path.parent/'narration_jp.wav'
    with wave.open(str(out),'wb') as audio:
        audio.setnchannels(channels);audio.setsampwidth(width);audio.setframerate(rate)
        for frames,_,_,_ in chunks:audio.writeframes(frames)
    for scene,(_,seconds,text,caption) in zip(plan['scenes'],chunks):
        scene.update(duration=seconds,narration=text,caption=caption)
    plan.update(narration_file=out.name,narration=''.join(t for _,_,t,_ in chunks),captions=' / '.join(c for _,_,_,c in chunks),expected_seconds=total,voice_metadata={'engine':'AivisSpeech','speaker':speaker['name'],'style':voice['name'],'model_commercial_rights':'UNVERIFIED','human_pronunciation_review':'PENDING'})
    path.write_text(json.dumps(plan,ensure_ascii=False,indent=2))
    print(json.dumps({'narration_file':str(out),'measured_duration':total,'rights':'UNVERIFIED','approval':'NOT_APPROVED'}))
if __name__=='__main__':
    import sys
    synthesize(sys.argv[1])
