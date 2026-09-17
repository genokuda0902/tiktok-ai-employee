#!/usr/bin/env python3
import json, os, time, urllib.parse, urllib.request, wave
from pathlib import Path
BASE=os.environ.get('AIVIS_URL','http://127.0.0.1:10101')
OUT=Path(os.environ.get('NARRATION_OUT','output/narration.wav')); OUT.parent.mkdir(parents=True,exist_ok=True)
PREFERRED_SPEAKER=os.environ.get('AIVIS_SPEAKER_NAME','Flow').strip().lower()
PREFERRED_STYLE=os.environ.get('AIVIS_STYLE_NAME','04_FUN').strip().lower()
# display=字幕・画面同期用 / speak=発音安定用。英字は日本語読みに固定。
CHUNKS=[
 {'display':'Excel作業に、時間を取られすぎていませんか？','speak':'エクセル作業に、時間を取られすぎていませんか？','pause':0.07},
 {'display':'その作業、AIなら一気に短縮できます。','speak':'その作業、エーアイなら、一気に短縮できます。','pause':0.07},
 {'display':'例えば売上データをChatGPTに貼り付けます。','speak':'例えば、売上データを、チャット・ジーピーティーに貼り付けます。','pause':0.06},
 {'display':'「グラフを作って、Excel形式で出して」と入力。','speak':'「グラフを作って、エクセル形式で出して」と入力。','pause':0.06},
 {'display':'すると、分析とグラフ作成が自動で進みます。','speak':'すると、分析とグラフ作成が、自動で進みます。','pause':0.06},
 {'display':'数秒で、グラフとExcel用データが完成。','speak':'数秒で、グラフと、エクセル用データが完成。','pause':0.06},
 {'display':'あとは、そのままExcelに貼り付けるだけ。','speak':'あとは、そのまま、エクセルに貼り付けるだけ。','pause':0.06},
 {'display':'見やすいグラフまで、すぐに作れます。','speak':'見やすいグラフまで、すぐに作れます。','pause':0.07},
 {'display':'手作業で数時間かかっていた仕事が、数分に。','speak':'手作業で、数時間かかっていた仕事が、数分に。','pause':0.07},
 {'display':'資料作成、メール、データ整理、アイデア出しにも使えます。','speak':'資料作成、メール、データ整理、アイデア出しにも使えます。','pause':0.07},
 {'display':'AIは、面倒な作業を減らしてくれる仕事の相棒です。','speak':'エーアイは、面倒な作業を減らしてくれる、仕事の相棒です。','pause':0.07},
 {'display':'明日使うなら保存してフォロー。AI時短ラボでまた。','speak':'明日使うなら、保存してフォロー。エーアイ時短ラボで、また。','pause':0.0},
]
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
 for sp in speakers:
  if PREFERRED_SPEAKER in str(sp.get('name','')).lower() and sp.get('styles'):
   for st in sp['styles']:
    if PREFERRED_STYLE in str(st.get('name','')).lower():
     print(f'Selected speaker={sp.get("name")} style={st.get("name")}'); return int(st['id'])
   print(f'Preferred style not found; using {sp["styles"][0].get("name")}')
   return int(sp['styles'][0]['id'])
 for sp in speakers:
  if sp.get('styles'):
   print(f'Preferred speaker not found; fallback={sp.get("name")}')
   return int(sp['styles'][0]['id'])
 raise RuntimeError('No AivisSpeech speaker styles available')
speakers=wait_engine(); style=choose_style(speakers)
parts=[]; timings=[]; cursor=0.0; sr=sw=ch=None
for item in CHUNKS:
 text=item['speak']; pause=item['pause']
 params=urllib.parse.urlencode({'text':text,'speaker':style})
 q=json.loads(req('/audio_query?'+params,method='POST').decode())
 q['speedScale']=float(os.environ.get('AIVIS_SPEED','1.13')); q['volumeScale']=1.0
 q['intonationScale']=float(os.environ.get('AIVIS_INTONATION','1.12'))
 raw=req('/synthesis?'+urllib.parse.urlencode({'speaker':style}),method='POST',data=json.dumps(q,ensure_ascii=False).encode(),content_type='application/json',timeout=300)
 tmp=OUT.parent/'_chunk.wav'; tmp.write_bytes(raw)
 with wave.open(str(tmp),'rb') as w:
  if sr is None: sr=w.getframerate(); sw=w.getsampwidth(); ch=w.getnchannels()
  data=w.readframes(w.getnframes()); seconds=w.getnframes()/w.getframerate()
 parts.append(data); timings.append({'text':item['display'],'speak':text,'start':round(cursor,3),'end':round(cursor+seconds,3),'style_id':style}); cursor+=seconds
 if pause: parts.append(b'\x00'*(int(sr*pause)*sw*ch)); cursor+=pause
 tmp.unlink(missing_ok=True)
with wave.open(str(OUT),'wb') as w:
 w.setparams((ch,sw,sr,0,'NONE','not compressed'))
 for p in parts:w.writeframes(p)
(OUT.parent/'narration_timing.json').write_text(json.dumps(timings,ensure_ascii=False,indent=2),encoding='utf-8')
if OUT.stat().st_size<1000:raise RuntimeError('Generated narration WAV is unexpectedly small')
print(f'Generated {OUT}; duration={cursor:.2f}s')
