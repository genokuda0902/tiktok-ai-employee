"""Review-only audio loudness normalization; audio presence is NOT Japanese narration verification."""
import argparse
import json
import subprocess

def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],text=True))

def normalize(src,dst):
    types={s["codec_type"] for s in probe(src)["streams"]}
    if not {"video","audio"} <= types:
        raise ValueError("video and audio streams required")
    subprocess.run(["ffmpeg","-y","-i",str(src),"-map","0:v:0","-map","0:a:0","-c:v","copy","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-c:a","aac","-b:a","128k","-movflags","+faststart",str(dst)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(dst),"-f","null","-"],check=True)
    return probe(dst)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source");p.add_argument("destination")
    a=p.parse_args()
    print(json.dumps(normalize(a.source,a.destination),ensure_ascii=False)[:500])
