"""Review-only three-scene renderer. Requires ffmpeg and Noto CJK fonts. No external assets."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'cycle1293_REVIEW_ONLY.mp4'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
scenes=[('AIの回答をそのまま使う前に','出典を確認'),('情報はいつのもの？','日付を確認'),('最後は自分で判断','根拠を残す')]
clips=[]
for i,(heading,detail) in enumerate(scenes):
    p=ROOT/f'scene_{i}.mp4'
    vf=(f"drawbox=x=80:y=360:w=920:h=1120:color=0x15283d:t=fill,"
        f"drawbox=x=80:y=360:w=18:h=1120:color=0x49c8e8:t=fill,"
        f"drawtext=fontfile={FONT}:text='{heading}':fontcolor=white:fontsize=54:x=(w-text_w)/2:y=630,"
        f"drawtext=fontfile={FONT}:text='{detail}':fontcolor=0xffe08a:fontsize=78:x=(w-text_w)/2:y=840,"
        f"drawtext=fontfile={FONT}:text='REVIEW ONLY / 未承認':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=1650,"
        f"drawbox=x=80:y=1540:w=920*min(t/3\\,1):h=10:color=0x49c8e8:t=fill")
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x091522:s=1080x1920:r=24:d=3','-vf',vf,'-an','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',str(p)],check=True)
    clips.append(p)
lst=ROOT/'concat.txt'
lst.write_text(''.join(f"file '{p}'\n" for p in clips))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(OUT)],check=True)
print(OUT)
