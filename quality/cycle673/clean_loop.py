"""Review-only crossfade ghosting fix for 9:16 video. Never posts."""
import argparse
import json
import subprocess
from pathlib import Path

def run(args):
    subprocess.run(args, check=True)

def probe(p):
    return json.loads(subprocess.check_output(
        ["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)],text=True))

def render(src,dst):
    src,dst=Path(src),Path(dst)
    if not src.is_file() or src.resolve()==dst.resolve():
        raise ValueError("Missing source or output overwrites source")
    m=probe(src)
    v=next(s for s in m["streams"] if s["codec_type"]=="video")
    if (v["width"],v["height"])!=(1080,1920):
        raise ValueError("Expected 1080x1920")
    if not any(s["codec_type"]=="audio" for s in m["streams"]):
        raise ValueError("Missing audio stream")
    if abs(float(m["format"]["duration"])-20)>0.1:
        raise ValueError("Expected 20 seconds")
    dst.parent.mkdir(parents=True,exist_ok=True)
    still=dst.with_suffix(".first.png")
    run(["ffmpeg","-v","error","-y","-i",str(src),"-frames:v","1",str(still)])
    fc=("[0:v]fps=30,trim=end_frame=576,setpts=PTS-STARTPTS,"
        "fade=t=out:st=18.98:d=0.22[a];"
        "[1:v]fps=30,trim=end_frame=24,setpts=PTS-STARTPTS,"
        "format=yuv420p,fade=t=in:st=0:d=0.22[b];"
        "[a][b]concat=n=2:v=1:a=0[v]")
    run(["ffmpeg","-v","error","-y","-i",str(src),
         "-loop","1","-framerate","30","-t","0.8","-i",str(still),
         "-filter_complex",fc,"-map","[v]","-map","0:a:0",
         "-c:v","libx264","-preset","veryfast","-crf","20",
         "-pix_fmt","yuv420p","-frames:v","600",
         "-c:a","aac","-b:a","160k","-movflags","+faststart",str(dst)])
    return {"output":str(dst),"publication":"NOT_APPROVED",
            "narration":"UNVERIFIED"}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output)))
