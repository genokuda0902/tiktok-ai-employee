"""Self-contained, review-only Japanese MP4. No external/private media."""
from pathlib import Path
import argparse, subprocess
SCENES=[("入力作業を減らす","架空データで試す"),("項目を整理","入力と出力を確認"),("処理をテスト","結果を人が点検"),("公開前に確認","個人情報と権利を確認")]
def make(output):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    clips=[]
    for i,(title,caption) in enumerate(SCENES):
        clip=output.parent/f"scene_{i}.mp4"
        def esc(s): return s.replace("\\","\\\\").replace(":","\\:").replace("'","’")
        vf=f"drawtext=fontfile={font}:text='{esc(title)}':fontsize=52:fontcolor=white:x=60:y=400,drawbox=x=30:y=940:w=660:h=140:color=black@0.85:t=fill,drawtext=fontfile={font}:text='{esc(caption)}':fontsize=36:fontcolor=white:x=60:y=980"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi","-i","color=c=0x101d35:s=720x1280:r=12:d=3","-vf",vf,"-an","-c:v","libx264","-pix_fmt","yuv420p",str(clip)],check=True)
        clips.append(clip)
    concat=output.parent/"concat.txt";concat.write_text("".join(f"file '{p.resolve()}'\n" for p in clips))
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(output)],check=True)
    return output
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--output",default="review.mp4");a=p.parse_args();print(make(a.output))
