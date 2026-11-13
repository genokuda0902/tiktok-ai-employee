"""Reproducible synthetic 9s vertical video with burned-in Japanese captions. REVIEW ONLY."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[("課題：手入力の集計","毎回、合計を計算していませんか？"),("実演：SUM関数",r"=SUM(B2\:B4)"),("結果：6,700","1,200 ＋ 2,300 ＋ 3,200")]
def render():
    clips=[]
    for i,(heading,caption) in enumerate(SCENES):
        dest=P/f"part{i}.mp4"
        vf=(f"drawbox=x=56:y=220:w=968:h=1380:color=0x132238:t=fill,"
            f"drawbox=x=56:y=220:w=968:h=12:color=0x46d3cb:t=fill,"
            f"drawtext=fontfile={FONT}:text='{heading}':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=430,"
            f"drawbox=x=78:y=1190:w=924:h=210:color=black@0.78:t=fill,"
            f"drawtext=fontfile={FONT}:text='{caption}':fontcolor=white:fontsize=43:x=(w-text_w)/2:y=1255,"
            f"drawtext=fontfile={FONT}:text='REVIEW ONLY - NO JAPANESE VOICE':fontcolor=0xffb4b4:fontsize=27:x=(w-text_w)/2:y=1720")
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi","-i","color=c=0x08111f:s=1080x1920:r=30:d=3","-vf",vf,"-an","-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p",str(dest)],check=True)
        clips.append(dest)
    listing=P/"concat.txt";listing.write_text("".join(f"file '{p}'\n" for p in clips))
    out=P/"cycle1438_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(listing),"-f","lavfi","-i","anullsrc=r=44100:cl=mono","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest","-movflags","+faststart",str(out)],check=True)
    (P/"captions.srt").write_text("".join(f"{i+1}\n00:00:{i*3:02},000 --> 00:00:{(i+1)*3:02},000\n{c.replace(chr(92)+':',':')}\n\n" for i,(_,c) in enumerate(SCENES)),encoding="utf-8")
    return out
if __name__=="__main__":print(render())
