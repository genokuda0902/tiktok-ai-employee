"""Review-only timed scene labels; these are NOT speech-synchronized subtitles."""
from pathlib import Path
import argparse, subprocess
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
STAGES=[(0,4,"計算前：120と180を入力"),(4,10,"操作：SUM関数を入力"),(10,15,"結果：合計300を確認")]
def validate(stages,duration):
    if not stages or stages[0][0]!=0 or stages[-1][1]!=duration: raise ValueError("coverage gap")
    for i,(start,end,label) in enumerate(stages):
        if start>=end or not label or (i and start!=stages[i-1][1]): raise ValueError("invalid timeline")
def render(src,dst):
    validate(STAGES,15)
    if not Path(src).is_file(): raise FileNotFoundError(src)
    filters=[]
    for start,end,label in STAGES:
        label=label.replace("\\","\\\\").replace(":","\\:").replace("'","’")
        filters.append(f"drawbox=x=24:y=h-205:w=672:h=122:color=black@0.82:t=fill:enable='between(t,{start},{end-0.04})'")
        filters.append(f"drawtext=fontfile={FONT}:text='{label}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=h-166:enable='between(t,{start},{end-0.04})'")
    filters.append(f"drawtext=fontfile={FONT}:text='レビュー専用・公開不可':fontcolor=white@0.7:fontsize=22:x=24:y=28")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),"-vf",",".join(filters),"-c:v","libx264","-preset","veryfast","-crf","24","-pix_fmt","yuv420p","-an","-movflags","+faststart",str(dst)],check=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("source");p.add_argument("output");a=p.parse_args();render(a.source,a.output)
