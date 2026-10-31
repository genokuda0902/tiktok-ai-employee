"""CI smoke: original prompt art -> 2s H264/AAC synthetic MP4 -> full decode."""
import json,subprocess,tempfile
from pathlib import Path
from prompt_component import render_art

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-1000:])
    return p.stdout

with tempfile.TemporaryDirectory() as tmp:
    folder=Path(tmp);img=folder/"prompt.png";out=folder/"smoke.mp4"
    render_art(2.3).resize((1080,1920)).save(img)
    run(["ffmpeg","-hide_banner","-loglevel","error","-y",
         "-loop","1","-framerate","30","-i",str(img),
         "-f","lavfi","-i","sine=frequency=440:sample_rate=48000",
         "-t","2","-c:v","libx264","-preset","ultrafast",
         "-pix_fmt","yuv420p","-c:a","aac","-shortest",str(out)])
    p=json.loads(run(["ffprobe","-v","error","-show_entries",
         "stream=codec_name,width,height,r_frame_rate,sample_rate:format=duration",
         "-of","json",str(out)]))
    v=p["streams"][0]
    assert v["codec_name"]=="h264" and (v["width"],v["height"])==(1080,1920)
    assert v["r_frame_rate"]=="30/1"
    assert any(s["codec_name"]=="aac" for s in p["streams"])
    run(["ffmpeg","-hide_banner","-loglevel","error","-xerror","-i",str(out),"-f","null","-"])
    print("PASS: 2s synthetic H264/AAC 1080x1920 full decode")
