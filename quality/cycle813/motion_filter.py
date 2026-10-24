"""Cycle813 offline cinematic motion pass. Never posts or approves content."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRES = ("ai_work","beauty","love_psychology","money_saving","sales_business",
          "career","health_life","science","travel_food","product_life")
STATUS = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"
VIDEO_FILTER = (
    "scale=1144:2034:flags=lanczos,"
    "crop=1080:1920:x='(in_w-out_w)/2+13*sin(n/42)':"
    "y='(in_h-out_h)/2+16*cos(n/55)',"
    "eq=contrast=1.025:saturation=1.045,"
    "unsharp=3:3:0.28:3:3:0.0,format=yuv420p"
)

def call(args, capture=False):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(" ".join(map(str,args)) + "\n" + p.stderr[-2000:])
    return p.stdout if capture else None

def probe(path):
    return json.loads(call(["ffprobe","-v","error","-show_streams","-show_format",
                            "-of","json",str(path)], True))

def audio_digest(path):
    p = subprocess.run(["ffmpeg","-v","error","-i",str(path),"-map","0:a:0",
                        "-c:a","copy","-f","adts","-"], capture_output=True, check=True)
    return hashlib.sha256(p.stdout).hexdigest()

def render(source, target):
    source, target = Path(source), Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    call(["ffmpeg","-y","-v","error","-i",str(source),"-vf",VIDEO_FILTER,
          "-map","0:v:0","-map","0:a:0","-c:v","libx264","-preset","veryfast",
          "-crf","19","-r","30","-c:a","copy","-movflags","+faststart",str(target)])
    call(["ffmpeg","-v","error","-xerror","-i",str(target),"-f","null","-"])
    src = probe(source); dst = probe(target)
    v = next(s for s in dst["streams"] if s["codec_type"]=="video")
    a = next(s for s in dst["streams"] if s["codec_type"]=="audio")
    sv = next(s for s in src["streams"] if s["codec_type"]=="video")
    assert (int(v["width"]),int(v["height"])) == (1080,1920)
    assert v["codec_name"] == "h264" and v["r_frame_rate"] == "30/1"
    assert int(v["nb_frames"]) == int(sv["nb_frames"])
    assert a["codec_name"] == "aac" and int(a["sample_rate"]) == 48000
    assert audio_digest(source) == audio_digest(target)
    return {"status":STATUS,"frames":int(v["nb_frames"]),
            "duration":float(dst["format"]["duration"]),
            "audio_unchanged":True,"resolution":[1080,1920]}

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    print(json.dumps(render(args.input,args.output),ensure_ascii=False))
