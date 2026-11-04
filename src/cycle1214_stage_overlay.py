"""Review-only three-stage overlay. No publication approval implied."""
import subprocess
from pathlib import Path
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def stage_filter():
    parts=[]
    for label,start,end in [("01 目的",7,9),("02 条件",9,11),("03 確認",11,13)]:
        enabled=f"between(t\\,{start}\\,{end})"
        parts.append(f"drawbox=x=100:y=1260:w=880:h=150:color=0x111827@0.92:t=fill:enable={enabled}")
        parts.append(f"drawtext=fontfile={FONT}:text='{label}':fontcolor=white:fontsize=66:x=(w-text_w)/2:y=1290:enable={enabled}")
    return ",".join(parts)
def render(src,dst):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),"-vf",stage_filter(),"-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(dst)],check=True)
