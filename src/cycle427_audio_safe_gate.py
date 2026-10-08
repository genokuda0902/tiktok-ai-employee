"""Cycle427: native Japanese TTS probe; fails closed if unavailable."""
from pathlib import Path
import numpy as np
import soundfile as sf

CAPTIONS = [
 "商談後の一通で、仕事の質は変わる。",
 "メモには、未決定の情報も混ざっています。",
 "AIには、決定と未決定を分けて伝えます。",
 "決定事項、確認事項、次の行動に整理。",
 "相手に送る文章は、短く具体的に。",
 "未確定の日時を、AIに決めさせない。",
 "送信前に、事実と相手と期限を確認。",
]

def synthesize(output="output/cycle427_japanese.wav"):
 from kokoro import KPipeline
 p=KPipeline(lang_code="j")
 clips=[]
 for caption in CAPTIONS:
  segments=[np.asarray(a,dtype=np.float32) for _,_,a in p(caption,voice="jf_alpha",speed=1.15)]
  if not segments: raise RuntimeError("empty Japanese speech")
  clips.append(np.concatenate(segments))
 path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
 sf.write(path,np.concatenate(clips),24000)
 return path
