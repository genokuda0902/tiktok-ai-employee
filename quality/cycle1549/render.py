"""Review-only burned Japanese captions; input MP4 must be approved and supplied locally."""
from pathlib import Path
import subprocess, sys
SOURCE=Path(sys.argv[1]); OUTPUT=Path(sys.argv[2])
CAPTIONS=[("00:00:00,000","00:00:03,000","合計を一瞬で計算"),("00:00:03,000","00:00:06,000","セルを選択する"),("00:00:06,000","00:00:09,000","SUM関数を入力"),("00:00:09,000","00:00:12,000","結果を確認する")]
def srt_text():
    return "".join(f"{i}\n{a} --> {b}\n{t}\n\n" for i,(a,b,t) in enumerate(CAPTIONS,1))
def render():
    if not SOURCE.is_file(): raise FileNotFoundError(SOURCE)
    srt=OUTPUT.with_suffix(".srt"); srt.write_text(srt_text(),encoding="utf-8")
    vf=f"subtitles={srt}:force_style='FontName=Noto Sans CJK JP,FontSize=20,Outline=2,Shadow=1,MarginV=195,Alignment=2'"
    subprocess.run(["ffmpeg","-y","-i",str(SOURCE),"-vf",vf,"-c:v","libx264","-crf","22","-c:a","copy","-movflags","+faststart",str(OUTPUT)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(OUTPUT),"-f","null","-"],check=True)
if __name__=="__main__":render()
