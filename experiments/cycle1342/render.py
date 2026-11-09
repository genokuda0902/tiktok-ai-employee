"""Review-only legibility overlay for synthetic/approved input. Requires ffmpeg and Noto CJK."""
from pathlib import Path
import subprocess,sys
INPUT=Path(sys.argv[1]) if len(sys.argv)>1 else Path("cycle1341_REVIEW_ONLY.mp4")
OUTPUT=Path(sys.argv[2]) if len(sys.argv)>2 else Path("cycle1342_REVIEW_ONLY.mp4")
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
CAPTIONS=[(0,3,"売上の合計を一瞬で出す"),(3,6,"合計したいセルを選ぶ"),(6,9,"SUM関数を入力する"),(9,12,"範囲を指定して確定"),(12,15,"計算結果を確認する")]
def caption_filter():
    parts=[]
    for start,end,line in CAPTIONS:
        enabled=f"between(t\\,{start}\\,{end-0.05})"
        parts.append(f"drawbox=x=72:y=1450:w=936:h=180:color=black@0.85:t=fill:enable={enabled}")
        parts.append(f"drawtext=fontfile={FONT}:text='{line}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=1512:enable={enabled}")
    return ",".join(parts)
def render():
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(INPUT),"-vf",caption_filter(),"-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-an","-movflags","+faststart",str(OUTPUT)],check=True)
if __name__=="__main__":render()
