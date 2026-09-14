#!/usr/bin/env python3
from pathlib import Path
import subprocess

out = Path('output')
out.mkdir(exist_ok=True)
audio = out / 'narration.wav'
video = out / 'AI時短ラボ_01_完成版.mp4'
if not audio.exists():
    raise SystemExit('Missing output/narration.wav')

# First reliable audio+video build. Visual layer is intentionally simple; v3 rich demo editing follows after pipeline passes.
filtergraph = "drawbox=x=70:y=160:w=12:h=1480:color=0x38d9ff:t=fill,drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='そのExcelコピペ':fontcolor=white:fontsize=76:x=(w-text_w)/2:y=610,drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='まだ手作業ですか？':fontcolor=0xffe66d:fontsize=82:x=(w-text_w)/2:y=720,drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc:text='AI時短ラボ':fontcolor=white@0.7:fontsize=38:x=(w-text_w)/2:y=1710"
cmd = [
    'ffmpeg','-y','-f','lavfi','-i','color=c=0x081426:s=1080x1920:r=30',
    '-i',str(audio),'-vf',filtergraph,'-map','0:v:0','-map','1:a:0',
    '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','160k','-ar','44100','-shortest','-movflags','+faststart',str(video)
]
subprocess.run(cmd, check=True)
print(video)
