from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro import KPipeline

OUT=Path("output"); OUT.mkdir(exist_ok=True)
pipeline=KPipeline(lang_code="j")
voice="jf_alpha"

tests = {
"01_plain": "そのコピペ、まだ手作業ですか？ AIに必要な項目を伝えて、表形式で整理してもらいます。あとはExcelに貼り付けるだけ。面倒な転記作業を減らせます。",
"02_spoken_words": "そのコピペ、まだ手作業ですか？ エーアイに必要な項目を伝えて、表形式で整理してもらいます。あとはエクセルに貼り付けるだけ。面倒な転記作業を減らせます。",
"03_short_phrases": "そのコピペ、まだ手作業ですか？\nエーアイに、必要な項目を伝えます。\n表形式で、整理してもらいます。\nあとは、エクセルに貼り付けるだけ。\n面倒な転記作業を、減らせます。",
"04_conversational": "そのコピペ、まだ手作業ですか？\n実は、エーアイに必要な項目を伝えるだけで大丈夫です。\n表に整理してもらって、あとはエクセルに貼り付けるだけ。\nこれだけで、面倒な転記作業をかなり減らせます。"
}

for name,text in tests.items():
    parts=[]
    for _,_,audio in pipeline(text, voice=voice, speed=1.0):
        parts.append(audio)
    if not parts:
        raise RuntimeError(name)
    sf.write(OUT/f"{name}.wav", np.concatenate(parts), 24000)

(OUT/"LISTEN_ORDER.txt").write_text(
"""同じ声質で読み方だけ比較します。
01 = 元の文章
02 = AI/Excelだけ読み表記化
03 = 文節を短くして間を調整
04 = TikTok向けの話し言葉へ変換

評価は「一番自然 / 全部微妙」だけでOKです。
""", encoding="utf-8")
