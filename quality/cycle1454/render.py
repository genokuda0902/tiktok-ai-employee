"""Self-contained review-only video; no external assets, no narration, no posting."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[("まだ手入力していますか？","表計算の時短テクニック"),("まず範囲を選択","合計したいセルを確認"),("SUM関数を入力","=SUM(B2:B6)"),("最後に検算","数字が合っているか確認")]
def render(output=ROOT/"cycle1454_REVIEW_ONLY.mp4"):
    clips=[]
    for i,(title,sub) in enumerate(SCENES):
        t=ROOT/f"title_{i}.txt";s=ROOT/f"sub_{i}.txt";t.write_text(title,encoding="utf8");s.write_text(sub,encoding="utf8")
        p=ROOT/f"clip_{i}.mp4"
        vf=f"drawbox=x=55:y=360:w=970:h=1150:color=0x14233c:t=fill,drawtext=fontfile={FONT}:textfile={t}:fontcolor=white:fontsize=62:x=(w-text_w)/2:y=640,drawtext=fontfile={FONT}:textfile={s}:fontcolor=0x9ce6e0:fontsize=40:x=(w-text_w)/2:y=890"
        subprocess.run(["ffmpeg","-nostdin","-y","-loglevel","error","-f","lavfi","-i","color=c=0x08111f:s=1080x1920:r=24:d=3.5","-vf",vf,"-c:v","libx264","-preset","ultrafast","-crf","27","-pix_fmt","yuv420p",str(p)],check=True)
        clips.append(p)
    listing=ROOT/"concat.txt";listing.write_text("".join(f"file '{p}'\n" for p in clips))
    subprocess.run(["ffmpeg","-nostdin","-y","-loglevel","error","-f","concat","-safe","0","-i",str(listing),"-c","copy","-movflags","+faststart",str(output)],check=True)
    for p in clips:p.unlink()
    return output
if __name__=="__main__":print(render())
