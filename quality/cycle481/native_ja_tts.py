#!/usr/bin/env python3
"""Native Japanese TTS proof. No paid API or publishing."""
from pathlib import Path
import argparse
import shutil
import subprocess
import wave

LINES = [
    "毎日のエクセル集計、まだ手作業ですか。",
    "最初に、日付、担当、件数の列をそろえます。",
    "次に、条件別の集計を数式に置き換えます。",
    "入力と集計の役割を分けて、更新を簡単にします。",
    "ただし、空欄と重複は必ず検算しましょう。",
    "まずは一つの集計から、仕組みを変えてみてください。",
]
def locate(patterns):
    for pattern in patterns:
        matches = sorted(Path("/usr/share").glob(pattern))
        if matches: return str(matches[0])
    raise FileNotFoundError("Open JTalk dictionary or HTS voice is missing")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="out")
    args = ap.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    if not shutil.which("open_jtalk"): raise RuntimeError("open_jtalk not installed")
    dic = locate(["open_jtalk/dic", "mecab/dic/open-jtalk/naist-jdic", "mecab/dic/open-jtalk"])
    voice = locate(["hts-voice/nitech-jp-atr503-m001/*.htsvoice", "open_jtalk/voices/**/*.htsvoice"])
    paths=[]
    for i,line in enumerate(LINES):
        wav = out / f"voice_{i:02d}.wav"
        subprocess.run(["open_jtalk","-x",dic,"-m",voice,"-r","1.1","-ow",str(wav)],
                       input=line+"\n",text=True,check=True)
        with wave.open(str(wav),"rb") as w:
            assert w.getnframes()>w.getframerate()//3, "empty voice"
        paths.append(wav)
    manifest = out/"voice_manifest.txt"
    manifest.write_text("\n".join(f"{p.name}: {line}" for p,line in zip(paths,LINES)),encoding="utf-8")
    print("PASS: generated",len(paths),"native Japanese speech WAV files")
if __name__ == "__main__": main()
