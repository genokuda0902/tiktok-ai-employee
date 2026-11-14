"""Review-only hook compositor. Requires an explicitly provided approved base MP4.
No narration is generated; publication is always blocked.
Usage: python quality/cycle1450/render.py --input base.mp4 --output review.mp4
"""
import argparse, json, subprocess, tempfile
from pathlib import Path
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
def run(args):
    subprocess.run(args,check=True)
def render(src,dst):
    src=Path(src); dst=Path(dst)
    if not src.is_file(): raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        hook=Path(temp)/"hook.mp4"
        vf=(f"drawtext=fontfile={FONT}:text='合計をまだ手入力？':fontcolor=white:fontsize=82:x=(w-text_w)/2:y=730,"
            f"drawtext=fontfile={REG}:text='12秒でSUM関数を確認':fontcolor=0x54e2cc:fontsize=52:x=(w-text_w)/2:y=900")
        run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=0x0b2235:s=1080x1920:r=24:d=1.5","-vf",vf,"-an","-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p",str(hook)])
        run(["ffmpeg","-y","-v","error","-i",str(hook),"-i",str(src),"-filter_complex","[0:v][1:v]concat=n=2:v=1:a=0[v]","-map","[v]","-c:v","libx264","-preset","ultrafast","-crf","24","-movflags","+faststart",str(dst)])
    run(["ffmpeg","-v","error","-i",str(dst),"-f","null","-"])
    return dst
def publication_approved(metadata):
    return all(metadata.get(k) is True for k in ("rights_approved","privacy_approved","japanese_voice_verified","speech_caption_sync_verified","employee_approved"))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--output",required=True)
    a=p.parse_args();print(render(a.input,a.output))
