#!/usr/bin/env python3
"""Offline Japanese TTS for cycle528. Requires open_jtalk + NAIST dictionary + HTS voice.
Review-only; no external API, posting or implicit approval.
"""
from pathlib import Path
import json, subprocess, shutil, glob, wave
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
LINES = [
"会議はしたのに、仕事が進まない。原因はメモかもしれません。",
"話したことだけを並べても、誰が何をするか分かりません。",
"一つ目。担当者を決めます。誰が動くのか、ひと目で分かるように。",
"二つ目。期限を決めます。いつまでにやるのか、日付を入れます。",
"三つ目。次の一歩を決めます。最初の作業まで、具体的に。",
"担当、期限、次の一歩。この三つがあれば、次の行動が見えます。",
"エーアイには、担当、期限、次の行動の三つに整理して、と頼みましょう。",
"会議メモは、行動につなげるために。保存して試してみてください。"
]
def prereq():
    engine = shutil.which("open_jtalk")
    dictionaries = ["/var/lib/mecab/dic/open-jtalk/naist-jdic", "/usr/share/open-jtalk/dic/naist-jdic"]
    dic = next((x for x in dictionaries if Path(x).is_dir()), None)
    voices = glob.glob("/usr/share/hts-voice/**/*.htsvoice", recursive=True)
    if not engine or not dic or not voices:
        raise RuntimeError(f"Japanese voice prerequisites unavailable: engine={engine} dic={dic} voices={len(voices)}")
    return engine, dic, voices[0]
def main():
    engine, dic, voice = prereq()
    OUT.mkdir(parents=True, exist_ok=True)
    qa = []
    for i, line in enumerate(LINES):
        path = OUT / f"ja_{i+1:02}.wav"
        subprocess.run([engine, "-x", dic, "-m", voice, "-r", "1.08", "-ow", str(path)], input=line+"\n", text=True, check=True)
        with wave.open(str(path), "rb") as w:
            duration = w.getnframes()/w.getframerate()
            assert w.getnframes()>w.getframerate() and 1 < duration < 20
        qa.append({"scene":i, "seconds":round(duration,3), "text":line})
    (OUT/"ja_voice_qa.json").write_text(json.dumps({"segments":qa,"human_listening":"PENDING","publication":"NOT_APPROVED"},ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__": main()
