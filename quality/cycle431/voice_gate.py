"""Fail-closed zero-cost Japanese narration. No auto-posting or publication approval."""
import json
from pathlib import Path
NARRATION=[
 "三泊四日の旅行。荷物が多すぎませんか？",
 "コツは、服、小物、充電器の三つです。",
 "服は、着回せる組み合わせを選びます。",
 "洗面用品と常備品は、分けてまとめます。",
 "充電器とコードは、同じポケットへ。",
 "荷物がすっきり。お土産の場所も確保。",
 "旅行前に、三つのポイントを確認。",
]
DURATIONS=[2.2,2.8,2.8,3.1,3.1,3.0,3.0]
def voice(output):
 import numpy as np
 import soundfile as sf
 from kokoro import KPipeline
 out=Path(output);out.mkdir(parents=True,exist_ok=True)
 pipe=KPipeline(lang_code="j")
 waves=[];log=[];sr=24000
 for i,(sentence,dur) in enumerate(zip(NARRATION,DURATIONS)):
  chunks=[audio for _,_,audio in pipe(sentence,voice="jf_alpha",speed=1.0)]
  if not chunks:raise RuntimeError(f"No Japanese speech for scene {i+1}")
  audio=np.concatenate(chunks).astype("float32")
  length=len(audio)/sr
  if length>dur:raise RuntimeError(f"Japanese speech too long in scene {i+1}: {length:.2f}s > {dur}s")
  padded=np.pad(audio,(0,int(round(dur*sr))-len(audio)))
  waves.append(padded)
  sf.write(out/f"scene_{i+1:02d}_ja.wav",audio,sr)
  log.append({"scene":i+1,"spoken_seconds":round(length,3),"slot_seconds":dur,"text":sentence})
 joined=np.concatenate(waves)
 if len(joined)!=20*sr:raise RuntimeError("duration mismatch")
 if np.max(np.abs(joined))<0.01:raise RuntimeError("TTS generated silence")
 sf.write(out/"cycle431_ja_narration.wav",joined,sr)
 (out/"voice_manifest.json").write_text(json.dumps({"voice":"jf_alpha","lang":"ja","human_listening_approved":False,"scenes":log},ensure_ascii=False,indent=2),encoding="utf-8")
 return out/"cycle431_ja_narration.wav"
if __name__=="__main__":
 print(voice("output/cycle431_ja"))
