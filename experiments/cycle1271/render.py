"""Reproducible review-only Japanese vertical video; deliberately NO narration."""
from pathlib import Path
import subprocess
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('AIの答え、即採用？','まずは立ち止まる'),('確認するのは3つ','出典・日付・数字'),('最後は人が判断','公開前に必ず確認')]
def render():
    clips=[]
    for i,(head,sub) in enumerate(SCENES):
        p=OUT/f'scene{i}.mp4'
        vf=(f"drawbox=x=70:y=280:w=940:h=1100:color=0x14243c:t=fill,"
            f"drawbox=x=70:y=280:w={int(940*(i+1)/3)}:h=14:color=0x50e3c2:t=fill,"
            f"drawtext=fontfile={FONT}:text='{head}':fontcolor=white:fontsize=74:x=(w-text_w)/2:y=640,"
            f"drawtext=fontfile={FONT}:text='{sub}':fontcolor=0x50e3c2:fontsize=48:x=(w-text_w)/2:y=810,"
            f"drawtext=fontfile={FONT}:text='REVIEW ONLY':fontcolor=white:fontsize=26:x=(w-text_w)/2:y=1640")
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0x08111e:s=1080x1920:r=30:d=3','-vf',vf,'-an','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',str(p)],check=True)
        clips.append(p)
    playlist=OUT/'concat.txt'
    playlist.write_text(''.join(f"file '{p.name}'\n" for p in clips))
    video=OUT/'cycle1271_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(playlist),'-c','copy','-movflags','+faststart',str(video)],check=True,cwd=OUT)
    (OUT/'captions.srt').write_text('1\n00:00:00,000 --> 00:00:03,000\nAIの答え、即採用？\n\n2\n00:00:03,000 --> 00:00:06,000\n確認するのは3つ\n\n3\n00:00:06,000 --> 00:00:09,000\n最後は人が判断\n',encoding='utf-8')
    return video
if __name__=='__main__':
    print(render())
