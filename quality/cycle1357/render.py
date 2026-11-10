"""Review-only native-resolution Japanese caption renderer. No narration; not approved for posting."""
from pathlib import Path
import subprocess

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
CAPTIONS = ["売上を一瞬で集計", "セルにSUM関数を入力", "=SUM(B2:B5)", "結果は 120,000円"]

def filtergraph():
    filters = []
    for i, caption in enumerate(CAPTIONS):
        escaped = caption.replace(":", r"\:").replace(",", r"\,")
        filters.append(f"drawtext=fontfile={FONT}:text='{escaped}':fontcolor=white:fontsize=65:x=(w-text_w)/2:y=1350:box=1:boxcolor=0x101a32@0.92:boxborderw=28:enable='between(t,{3*i},{3*(i+1)})'")
    filters.append("drawbox=x=70:y=1680:w=940:h=12:color=0x334155:t=fill")
    return ",".join(filters)

def render(output: Path):
    subprocess.run(["ffmpeg","-y","-f","lavfi","-i","color=c=0x0b152a:s=1080x1920:r=24:d=12","-vf",filtergraph(),"-c:v","libx264","-preset","ultrafast","-crf","25","-pix_fmt","yuv420p","-an","-movflags","+faststart",str(output)],check=True)

if __name__ == "__main__":
    render(Path("cycle1357_REVIEW_ONLY.mp4"))
