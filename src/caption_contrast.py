"""Safe-area contrast overlay for review-only vertical video captions."""
import subprocess
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def filtergraph(text="重要なポイントを確認"):
    if not text or len(text)>32 or any(c in text for c in "':\\%,\n"):
        raise ValueError("caption must be short and FFmpeg-safe")
    return ("drawbox=x=90:y=1400:w=900:h=190:color=black@0.72:t=fill:enable='between(t,17,20)',"
            "drawbox=x=90:y=1400:w=9:h=190:color=0x35D0D0:t=fill:enable='between(t,17,20)',"
            f"drawtext=fontfile={FONT}:text='{text}':fontcolor=white:fontsize=54:"
            "x=(w-text_w)/2:y=1460:enable='between(t,17,20)'")
def render(source,target):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
        "-vf",filtergraph(),"-c:v","libx264","-preset","ultrafast","-crf","25",
        "-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(target)],check=True)
