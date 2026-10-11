"""Cycle506 native Japanese voice source: separate from phonetic local preview.
Requires Kokoro model and Japanese dictionary; no paid services.
Generated samples are REVIEW_ONLY and not publication-approved.
"""
from pathlib import Path
import json
import numpy as np
import soundfile as sf
from kokoro import KPipeline
LINES = [
"机の上、探し物だらけ？　まずは、置き場所を決めよう。",
"机を、使う、しまう、保留の、三つに分けます。",
"毎日使う物だけ、手の届く場所へ。",
"たまに使う物は、引き出しにまとめます。",
"迷う物は、保留ボックスへ。あとで見直します。",
"置き場所が決まると、片づけやすくなります。",
"終業前、三十秒だけ、元の場所に戻します。",
"使う、しまう、保留。保存して、試してみて。",
]
def main():
    out=Path("quality_cycles/cycle506/voice_output")
    out.mkdir(parents=True,exist_ok=True)
    pipeline=KPipeline(lang_code="j")
    records=[]
    for i,line in enumerate(LINES):
        parts=[a for _,_,a in pipeline(line,voice="jf_alpha",speed=1.12)]
        if not parts: raise RuntimeError(f"no audio at scene {i}")
        audio=np.concatenate(parts).astype("float32")
        if not len(audio) or np.max(np.abs(audio))<.001: raise RuntimeError(f"silent scene {i}")
        sf.write(out/f"scene_{i:02}.wav",audio,24000)
        records.append({"scene":i,"text":line,"duration_seconds":round(len(audio)/24000,3),"human_listened":False})
    (out/"manifest.json").write_text(json.dumps({"native_tts_engine":"Kokoro","voice":"jf_alpha","publishable":False,"records":records},ensure_ascii=False,indent=2),encoding="utf8")
    print(json.dumps({"segments":len(records),"durations":[r["duration_seconds"] for r in records]}))
if __name__=="__main__":main()
