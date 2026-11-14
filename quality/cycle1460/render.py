"""Rights-safe, self-contained synthetic UI review renderer. No voice; not publishable."""
from pathlib import Path
import subprocess
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def render(output):
    filters=["drawbox=x=65:y=300:w=950:h=1190:color=0x15233a:t=fill"]
    for y in range(400,1300,100):
        filters.append(f"drawbox=x=95:y={y}:w=890:h=90:color=0x1e293b:t=fill")
    for text,y in [("仕事の手入力を減らす",130),("作業を分解する",1540),("AIで下書きを作る",1640),("最後は人が確認",1740)]:
        filters.append(f"drawtext=fontfile={FONT}:text={text}:x=100:y={y}:fontsize=48:fontcolor=white")
    subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=0x080f20:s=1080x1920:r=24:d=12","-vf",",".join(filters),"-an","-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(output)],check=True)
if __name__=="__main__":
    render(Path("cycle1460_REVIEW_ONLY.mp4"))
