"""Original, review-only Japanese slide renderer. No private assets or posting."""
from pathlib import Path
import subprocess
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('AIの回答、そのまま使う？','最初の3秒で疑問を提示'),('まず、出典を確認','根拠のない数字は使わない'),('次に、日付を確認','古い情報は更新が必要'),('最後は、人が判断','仕事で使う前に確認しよう')]
def render():
    clips=[]
    for i,(title,subtitle) in enumerate(SCENES):
        path=OUT/f'scene{i}.mp4'
        vf=(f"drawbox=x=65:y=270:w=950:h=1250:color=0x14213d:t=fill,"
            f"drawbox=x=65:y=270:w=15:h=1250:color=0x39d6c3:t=fill,"
            f"drawtext=fontfile={FONT}:text='{title}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=620,"
            f"drawtext=fontfile={FONT}:text='{subtitle}':fontcolor=0xd0e4f5:fontsize=37:x=(w-text_w)/2:y=830,"
            f"drawtext=fontfile={FONT}:text='{i+1} / 4':fontcolor=0x39d6c3:fontsize=38:x=(w-text_w)/2:y=1340")
        subprocess.run(['ffmpeg','-loglevel','error','-y','-f','lavfi','-i','color=c=0x08111f:s=1080x1920:r=24:d=3','-vf',vf,'-c:v','libx264','-preset','ultrafast','-crf','26','-pix_fmt','yuv420p','-an',str(path)],check=True)
        clips.append(path)
    listing=OUT/'concat.txt'
    listing.write_text(''.join(f"file '{p}'\n" for p in clips))
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(OUT/'cycle1299_REVIEW_ONLY.mp4')],check=True)
    (OUT/'captions.srt').write_text(''.join(f'{i+1}\n00:00:{i*3:02},000 --> 00:00:{(i+1)*3:02},000\n{a}\n\n' for i,(a,_) in enumerate(SCENES)),encoding='utf8')
if __name__=='__main__': render()
