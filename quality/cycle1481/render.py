"""Review-only reproducible synthetic 9:16 video. No narration or approval."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('入力がバラバラ','毎回、集計に時間がかかる'),('条件をそろえる','列名と集計条件を統一'),('結果を確認する','元データと照合して判断'),('小さく改善する','次の作業に活かす')]
def render():
    ROOT.mkdir(parents=True,exist_ok=True)
    clips=[]
    for i,(h,b) in enumerate(SCENES):
        p=ROOT/f'scene{i}.mp4'
        vf=(f"drawbox=x=72:y=230:w=936:h=1360:color=0x17233b@0.96:t=fill,"
            f"drawbox=x=72:y=230:w=16:h=1360:color=0x3dd5d0:t=fill,"
            f"drawbox=x='130+min(t*120,160)':y=1040:w=540:h=32:color=0x3dd5d0:t=fill,"
            f"drawtext=fontfile={FONT}:text='STEP {i+1} / 4':fontsize=44:fontcolor=0x3dd5d0:x=135:y=365,"
            f"drawtext=fontfile={FONT}:text='{h}':fontsize=72:fontcolor=white:x=135:y=560,"
            f"drawtext=fontfile={FONT}:text='{b}':fontsize=40:fontcolor=white:x=135:y=790,"
            f"drawtext=fontfile={FONT}:text='架空データ・レビュー専用':fontsize=32:fontcolor=0xb5bfd0:x=135:y=1430")
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0x080f20:s=1080x1920:r=24:d=3','-vf',vf,'-c:v','libx264','-preset','ultrafast','-crf','27','-pix_fmt','yuv420p','-an',str(p)],check=True)
        clips.append(p)
    listing=ROOT/'concat.txt'
    listing.write_text(''.join(f"file '{p}'\n" for p in clips))
    out=ROOT/'cycle1481_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(out)],check=True)
    (ROOT/'captions.srt').write_text(''.join(f"{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{a}。{b}。\n\n" for i,(a,b) in enumerate(SCENES)),encoding='utf-8')
    for p in clips+[listing]: p.unlink()
    return out
if __name__=='__main__':print(render())
