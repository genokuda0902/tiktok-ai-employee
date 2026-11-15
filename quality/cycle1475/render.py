"""Review-only timed captions. Synthetic, approved input only. No publication."""
import argparse, subprocess
from pathlib import Path
SCENES=[(0,3,"入力データは架空の例です"),(3,6,"整理したい項目を指定"),(6,9,"表に変換して確認"),(9,12,"変更前と変更後を比較"),(12,15,"必ず人が内容を確認")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def srt():
    def stamp(t): return f"00:00:{t:02d},000"
    return "".join(f"{i}\n{stamp(a)} --> {stamp(b)}\n{txt}\n\n" for i,(a,b,txt) in enumerate(SCENES,1))
def render(src,dst):
    if not Path(src).is_file(): raise FileNotFoundError(src)
    vf=[]
    for a,b,txt in SCENES:
        vf.append(f"drawbox=x=80:y=1480:w=920:h=180:color=black@0.87:t=fill:enable='between(t,{a},{b-.001})'")
        vf.append(f"drawtext=fontfile={FONT}:text='{txt}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=1540:enable='between(t,{a},{b-.001})'")
    subprocess.run(["ffmpeg","-y","-i",src,"-vf",",".join(vf),"-an","-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",dst],check=True)
    Path(dst).with_suffix(".srt").write_text(srt(),encoding="utf-8")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("source");p.add_argument("output");a=p.parse_args();render(a.source,a.output)
