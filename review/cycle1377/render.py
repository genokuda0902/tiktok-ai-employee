"""Reproducible synthetic captioned review video, requires ffmpeg + Noto CJK fonts.
No narration, no posting approval. Run: python review/cycle1377/render.py
"""
from pathlib import Path
import subprocess, json
ROOT=Path(__file__).resolve().parent
ROOT.mkdir(parents=True,exist_ok=True)
scenes=["毎日の集計、手作業？","数字を入力","SUMで合計","結果を確認"]
captions=["毎日の売上集計、まだ手作業ですか？","架空の売上データを入力します","SUM関数で合計を計算します","合計4,500円。最後に数字を確認しましょう"]
font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
for i,(heading,caption) in enumerate(zip(scenes,captions)):
    (ROOT/f"heading{i}.txt").write_text(heading,encoding="utf-8")
    (ROOT/f"caption{i}.txt").write_text(caption,encoding="utf-8")
    vf=(f"drawtext=fontfile={font}:textfile={ROOT}/heading{i}.txt:fontcolor=white:fontsize=54:x=60:y=330,"
        f"drawbox=x=30:y=1450:w=1020:h=220:color=0x17253a:t=fill,"
        f"drawtext=fontfile={font}:textfile={ROOT}/caption{i}.txt:fontcolor=white:fontsize=37:x=60:y=1510")
    subprocess.run(["ffmpeg","-y","-f","lavfi","-i","color=c=0x0c1425:s=1080x1920:r=24:d=2",
                    "-vf",vf,"-an","-c:v","libx264","-pix_fmt","yuv420p",str(ROOT/f"scene{i}.mp4")],check=True)
(ROOT/"concat.txt").write_text("".join(f"file 'scene{i}.mp4'\n" for i in range(4)),encoding="utf-8")
out=ROOT/"cycle1377_REVIEW_ONLY.mp4"
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(ROOT/"concat.txt"),"-c","copy","-movflags","+faststart",str(out)],check=True)
(ROOT/"manifest.json").write_text(json.dumps({"publication_allowed":False,"narration_verified":False,"speech_synced_captions":False,"burned_timed_explanatory_captions":True,"employee_approved":False},ensure_ascii=False,indent=2))
print(out)
