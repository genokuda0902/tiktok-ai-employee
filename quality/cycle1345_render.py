"""Review-only synthetic interaction animation. Never label this publishable."""
from pathlib import Path
import subprocess

def render(output: Path):
    font="/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
    vf=(
        "drawbox=x=75:y=570:w=930:h=660:color=0x14243b@0.94:t=fill,"
        "drawbox=x=100:y=680:w=870:h=95:color=0x293e55:t=fill,"
        f"drawtext=fontfile={font}:text='売上の合計を確認':fontsize=62:fontcolor=white:x=110:y=370,"
        f"drawtext=fontfile={font}:text='=SUM(B2\\,B3\\,B4)':fontsize=54:fontcolor=white:x=135:y=695:enable='between(t,4,15)',"
        "drawbox=x='135+min(max(t-4,0),5)*105':y=790:w=12:h=80:color=0x22d3ee:t=fill:enable='between(t,4,10)',"
        f"drawtext=fontfile={font}:text='架空データの操作イメージ':fontsize=38:fontcolor=0xf9d77e:x=120:y=1070,"
        f"drawtext=fontfile={font}:text='音声未実装・レビュー専用':fontsize=40:fontcolor=0xffaaaa:x=110:y=1550"
    )
    subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i",
        "color=c=0x071323:s=1080x1920:r=30:d=15","-vf",vf,"-an",
        "-c:v","libx264","-preset","ultrafast","-crf","26",
        "-pix_fmt","yuv420p","-movflags","+faststart",str(output)],check=True)

if __name__=="__main__":
    render(Path("cycle1345_REVIEW_ONLY.mp4"))
