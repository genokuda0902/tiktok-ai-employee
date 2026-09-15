#!/usr/bin/env python3
import json, os, time, urllib.parse, urllib.request, wave
from pathlib import Path
BASE=os.environ.get('AIVIS_URL','http://127.0.0.1:10101')
OUT=Path(os.environ.get('NARRATION_OUT','output/narration.wav')); OUT.parent.mkdir(parents=True,exist_ok=True)
CHUNKS=[
('そのExcelコピペ、まだ手作業？',0.10),
('例えば、このバラバラな顧客情報。',0.08),
('普通なら、一件ずつExcelに移しますよね。',0.08),
('でもAIなら、元の文章をそのまま貼って、',0.05),
('氏名、電話番号、メール、希望日時を、表にして。これだけ。',0.10),
('はい。もう整理できました。',0.08),
('あとは内容を確認して、コピー。',0.06),
('Excelに貼り付けるだけ。',0.08),
('問い合わせ整理や、営業リストでも使えます。',0.08),
('明日会社で使うなら、保存して試してみて。',0.0)]
def req(path,method='GET',data=None,content_type=None,timeout=120):
 headers={'Content-Type':content_type} if content_type else {}
 r=urllib.request.Request(BASE+path,data=data,headers=headers,method=method)
 with urllib.request.urlopen(r,timeout=timeout) as res:return res.read()
def wait_engine():
 last=None
 for _ in range(60):
  try:return json.loads(req('/speakers',timeout=5).decode())
  except Exception as e:last=e;time.sleep(2)
 raise RuntimeError(f'AivisSpeech Engine not ready: {last}')
def choose_style(speakers):
 wanted=os.environ.get('AIVIS_STYLE_ID')
 if wanted:return int(wanted)
 for sp in speakers:
  if '中2' in str(sp.get('name','')) and sp.get('styles'):return int(sp['styles'][0]['id'])
 for sp in speakers:
  if sp.get('styles'):return int(sp['styles'][0]['id'])
 return 604166016
speakers=wait_engine(); style=choose_style(speakers); print(f'Using AivisSpeech style_id={style}')
parts=[]; timings=[]; cursor=0.0; sr=None; sw=None; ch=None
for text,pause in CHUNKS:
 params=urllib.parse.urlencode({'text':text,'speaker':style})
 q=json.loads(req('/audio_query?'+params,method='POST').decode())
 q['speedScale']=float(os.environ.get('AIVIS_SPEED','1.18')); q['volumeScale']=1.0
 body=json.dumps(q,ensure_ascii=False).encode()
 raw=req('/synthesis?'+urllib.parse.urlencode({'speaker':style}),method='POST',data=body,content_type='application/json',timeout=300)
 tmp=OUT.parent/'_chunk.wav'; tmp.write_bytes(raw)
 with wave.open(str(tmp),'rb') as w:
  if sr is None: sr=w.getframerate(); sw=w.getsampwidth(); ch=w.getnchannels()
  data=w.readframes(w.getnframes()); seconds=w.getnframes()/w.getframerate()
 parts.append(data); timings.append({'text':text,'start':round(cursor,3),'end':round(cursor+seconds,3)})
 cursor+=seconds
 if pause:
  silence=b'\x00'*(int(sr*pause)*sw*ch); parts.append(silence); cursor+=pause
 tmp.unlink(missing_ok=True)
with wave.open(str(OUT),'wb') as w:
 w.setparams((ch,sw,sr,0,'NONE','not compressed'))
 for p in parts:w.writeframes(p)
(OUT.parent/'narration_timing.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2),encoding='utf-8')
if OUT.stat().st_size<1000:raise RuntimeError('Generated narration WAV is unexpectedly small')
print(f'Generated {OUT}; duration={cursor:.2f}s')
