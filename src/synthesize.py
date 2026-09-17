#!/usr/bin/env python3
import json, os, time, urllib.parse, urllib.request, wave
from pathlib import Path
BASE=os.environ.get('AIVIS_URL','http://127.0.0.1:10101')
OUT=Path(os.environ.get('NARRATION_OUT','output/narration.wav')); OUT.parent.mkdir(parents=True,exist_ok=True)
PREFERRED_SPEAKER=os.environ.get('AIVIS_SPEAKER_NAME','まお').strip().lower()
PREFERRED_STYLE=os.environ.get('AIVIS_STYLE_NAME','ふつー').strip().lower()
# display=字幕用 / speak=発音安定用。英字をそのまま読ませず日本語読みに固定する。
CHUNKS=[
 {'display':'資料作成や売上データの集計、毎回時間かかってませんか？','speak':'資料作成や、売上データの集計。毎回、時間かかってませんか？','pause':0.10},
 {'display':'これ、ChatGPT×Excelで一気にラクになります。','speak':'これ、チャット・ジーピーティーと、エクセルで、一気にラクになります。','pause':0.10},
 {'display':'売上データを貼って「要点とグラフを作って」と入力。','speak':'売上データを貼って、「要点とグラフを作って」と入力。','pause':0.08},
 {'display':'AIがデータを読み込んで分析。','speak':'エーアイが、データを読み込んで、分析。','pause':0.08},
 {'display':'月別の売上推移と要点まで整理してくれます。','speak':'月ごとの売上推移と、要点まで、整理してくれます。','pause':0.08},
 {'display':'あとは結果をExcelに貼り付けるだけ。','speak':'あとは結果を、エクセルに、貼り付けるだけ。','pause':0.08},
 {'display':'グラフまで完成。資料づくりが一気に進みます。','speak':'グラフまで完成。資料づくりが、一気に進みます。','pause':0.10},
 {'display':'何時間もかけていた集計作業を短縮できます。','speak':'何時間もかけていた、集計作業を、短縮できます。','pause':0.08},
 {'display':'要約・メール作成・データの見える化にも応用できます。','speak':'要約、メール作成、データの見える化にも、応用できます。','pause':0.08},
 {'display':'明日の仕事で使うなら、保存して試してみて。','speak':'明日の仕事で使うなら、保存して、試してみて。','pause':0.0},
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
   return int(sp['styles'][0]['id'])
 for sp in speakers:
  if sp.get('styles'): return int(sp['styles'][0]['id'])
 raise RuntimeError('No AivisSpeech speaker styles available')
speakers=wait_engine(); style=choose_style(speakers)
parts=[]; timings=[]; cursor=0.0; sr=sw=ch=None
for item in CHUNKS:
 text=item['speak']; pause=item['pause']
 params=urllib.parse.urlencode({'text':text,'speaker':style})
 q=json.loads(req('/audio_query?'+params,method='POST').decode())
 q['speedScale']=float(os.environ.get('AIVIS_SPEED','1.10')); q['volumeScale']=1.0
 q['intonationScale']=float(os.environ.get('AIVIS_INTONATION','1.06'))
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
