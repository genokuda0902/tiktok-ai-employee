"""Cycle719 Japanese narration segments. Generates WAVs for human listening only."""
from pathlib import Path
import json
LINES=[
 "この基板、実はパソコン。",
 "手のひらサイズ、でも本格派。",
 "画面につなげば、操作できる。",
 "必要なのは、三つの接続。",
 "LEDも光らせられる。",
 "入力、処理、出力。",
 "最初は、たった一行。",
 "保存して、あとで試そう。",
]
def generate(out="output/cycle719_tts",voice="jf_alpha",speed=1.15):
 import numpy as np
 import soundfile as sf
 from kokoro import KPipeline
 p=Path(out);p.mkdir(parents=True,exist_ok=True)
 pipeline=KPipeline(lang_code="j")
 result=[]
 for i,line in enumerate(LINES,1):
  chunks=[np.asarray(audio,dtype=np.float32) for _,_,audio in pipeline(line,voice=voice,speed=speed)]
  if not chunks:raise RuntimeError(f"Empty Japanese audio scene {i}")
  samples=np.concatenate(chunks)
  if not np.isfinite(samples).all() or len(samples)<12000:raise RuntimeError(f"Invalid scene {i}")
  path=p/f"scene_{i:02d}.wav"
  sf.write(path,samples,24000)
  result.append({"scene":i,"text":line,"file":path.name,"duration_s":round(len(samples)/24000,3)})
 (p/"timings.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
 print("generated Japanese narration segments",len(result))
 return result
if __name__=="__main__":generate()
