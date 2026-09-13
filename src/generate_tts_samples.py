from pathlib import Path
import numpy as np, soundfile as sf
from kokoro import KPipeline
OUT=Path("output"); OUT.mkdir(exist_ok=True)
tests=[("01_hook","そのコピペ、まだ手作業ですか？"),("02_ai","エーアイに必要な項目を伝えて、表形式で整理してもらいます。"),("03_excel","あとはエクセルに貼り付けるだけ。面倒な転記作業を減らせます。"),("04_cta","保存して、あとで試してみてください。")]
pipeline=KPipeline(lang_code="j")
for voice in ["jf_alpha","jf_gongitsune","jm_kumo"]:
    for name,text in tests:
        parts=[audio for _,_,audio in pipeline(text,voice=voice,speed=1.05)]
        if not parts: raise RuntimeError(f"No audio: {voice}/{name}")
        sf.write(OUT/f"{voice}_{name}.wav",np.concatenate(parts),24000)
