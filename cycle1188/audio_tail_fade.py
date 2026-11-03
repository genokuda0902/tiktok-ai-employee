"""Review-only audio tail fade; preserves video bitstream. Not publication approval."""
import argparse
import json
import subprocess

def fade_start(duration: float, fade_seconds: float = 0.35) -> float:
    if duration <= 0 or fade_seconds <= 0 or fade_seconds > duration:
        raise ValueError("invalid duration/fade")
    return round(duration - fade_seconds, 3)

def run(src: str, dst: str, fade_seconds: float = 0.35) -> None:
    p = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",src],check=True,capture_output=True,text=True)
    duration = float(json.loads(p.stdout)["format"]["duration"])
    start = fade_start(duration, fade_seconds)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",src,"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f"afade=t=out:st={start}:d={fade_seconds}","-c:a","aac","-b:a","160k","-movflags","+faststart",dst],check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("dst")
    parser.add_argument("--fade",type=float,default=0.35)
    args = parser.parse_args()
    run(args.src,args.dst,args.fade)
