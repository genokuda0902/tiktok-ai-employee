"""Cycle1470: public-safe synthetic review render, no narration, NOT FOR POSTING."""
from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[("AIで作業を短縮","最初に目的を決める"),("入力は架空データ","個人情報を入れない"),("表形式で整理する","結果を人が確認する"),("公開前に承認","投稿は社員が手動で")]
def run():
    ROOT.mkdir(parents=True,exist_ok=True)
    parts=[]
    for i,(title,caption) in enumerate(SCENES):
        path=ROOT/f"part{i}.mp4"
        vf=f"drawbox=x=40:y=230:w=640:h=820:color=0x15253e:t=fill,drawbox=x=40:y=230:w=640:h=9:color=0x43d9cb:t=fill,drawtext=fontfile={FONT}:text='{title}':fontsize=44:fontcolor=white:x=(w-text_w)/2:y=360,drawtext=fontfile={FONT}:text='{caption}':fontsize=30:fontcolor=white:x=(w-text_w)/2:y=515,drawbox=x=90:y=700:w=540:h=90:color=0x263c59:t=fill,drawbox=x=90:y=700:w=540*min(t/2.5\\,1):h=90:color=0x157c83:t=fill"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi","-i","color=c=0x0b1427:s=720x1280:r=20:d=2.5","-vf",vf,"-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p","-an",str(path)],check=True)
        parts.append(path)
    concat=ROOT/"concat.txt"
    concat.write_text("".join(f"file '{p.name}'\\n" for p in parts))
    output=ROOT/"cycle1470_REVIEW_ONLY.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(output)],check=True,cwd=ROOT)
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_name,width,height,codec_type","-of","json",str(output)],text=True))
    (ROOT/"probe.json").write_text(json.dumps(probe,indent=2))
    subprocess.run(["ffmpeg","-v","error","-i",str(output),"-f","null","-"],check=True)
    for p in parts:p.unlink()
    concat.unlink()
    return probe
if __name__=="__main__":print(run())
