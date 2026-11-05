"""Review-only reusable opening hook overlay; not an approval gate."""
import subprocess
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def filtergraph(start=0.3,end=3.3):
    if not (0 <= start < end): raise ValueError("invalid interval")
    active=f"between(t,{start},{end})"
    return (f"drawbox=x=82:y=220:w=916:h=210:color=0x091525@0.88:t=fill:enable='{active}',"
            f"drawbox=x=82:y=220:w=12:h=210:color=0xffd166:t=fill:enable='{active}',"
            f"drawtext=fontfile={FONT}:text='AIの回答、そのまま使う？':fontcolor=white:fontsize=53:x=125:y=265:enable='{active}',"
            f"drawtext=fontfile={FONT}:text='3つの確認でミスを防ぐ':fontcolor=0xffd166:fontsize=42:x=125:y=345:enable='{active}'")
def render(source,output):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-vf",filtergraph(),"-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(output)],check=True)
