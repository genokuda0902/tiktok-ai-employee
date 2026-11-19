"""Reusable five-slide takeaway overlay. Requires ffmpeg and a Japanese font."""
import subprocess
from pathlib import Path

TAKEAWAYS = [
    "最初の3秒で目的を伝える",
    "写真は主役を大きく見せる",
    "声は聞き取りやすい音量に",
    "字幕は短く、一目で読める長さに",
    "公開前に映像と音声を確認",
]

def render(source: str, output: str, font: str, takeaways=TAKEAWAYS, duration=22.68):
    if len(takeaways) != 5:
        raise ValueError("Five slide takeaways required")
    filters = []
    for i, phrase in enumerate(takeaways):
        start, end = i * duration / 5, (i + 1) * duration / 5
        enable = f"between(t,{start:.3f},{end:.3f})"
        if any(c in phrase for c in "':\\"):
            raise ValueError("Unsupported unescaped text")
        filters += [
            f"drawbox=x=94:y=990:w=890:h=270:color=0x001b20@0.98:t=fill:enable='{enable}'",
            f"drawtext=fontfile='{font}':text='要点 {i+1} / 5':fontsize=32:fontcolor=0x7be6cc:x=120:y=1030:enable='{enable}'",
            f"drawtext=fontfile='{font}':text='{phrase}':fontsize=41:fontcolor=white:x=120:y=1115:enable='{enable}'",
        ]
    subprocess.run(["ffmpeg","-y","-i",source,"-vf",",".join(filters),
                    "-c:v","libx264","-preset","ultrafast","-crf","20",
                    "-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",output],check=True)
