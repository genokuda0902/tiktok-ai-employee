"""Cycle771 review-only MP4 composer. Keeps every AAC packet intact."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image
from outro_contract import validate, START_FRAME, END_FRAME
from outro_frames import frame

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def cmd(args):
    subprocess.run(args,check=True)

def render(source,manifest,out,work):
    source,manifest,out,work=map(Path,(source,manifest,out,work))
    m=json.loads(manifest.read_text(encoding="utf-8"))
    validate(m)
    if m.get("source_sha256")!=sha(source):
        raise ValueError("source SHA mismatch")
    work.mkdir(parents=True,exist_ok=True)
    out.parent.mkdir(parents=True,exist_ok=True)
    hero=work/"hero_local_only.png"
    cmd(["ffmpeg","-y","-v","error","-ss","1.2","-i",str(source),"-frames:v","1",str(hero)])
    with Image.open(hero) as img:
        for i in range(END_FRAME-START_FRAME):
            frame(img,i,m["genre"]).save(work/f"{i:04d}.jpg",quality=91,subsampling=0)
    video_only=work/"video_only.mp4"
    cmd(["ffmpeg","-y","-v","error","-i",str(source),
         "-itsoffset","24.3","-framerate","30","-i",str(work/"%04d.jpg"),
         "-filter_complex","[0:v][1:v]overlay=eof_action=pass:shortest=0:format=auto,format=yuv420p[v]",
         "-map","[v]","-c:v","libx264","-preset","ultrafast","-crf","20",
         "-an","-r","30","-frames:v","819",str(video_only)])
    cmd(["ffmpeg","-y","-v","error","-i",str(video_only),"-i",str(source),
         "-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","copy",
         "-movflags","+faststart",str(out)])
    video_only.unlink()
    print(json.dumps({"mp4_sha256":sha(out),"review_only":True}))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    for key in ["source","manifest","out","work"]:ap.add_argument("--"+key,required=True)
    a=ap.parse_args()
    render(a.source,a.manifest,a.out,a.work)
