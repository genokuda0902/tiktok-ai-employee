"""Generate and fully decode a 2s synthetic H264/AAC vertical MP4."""
import json,subprocess,tempfile
from pathlib import Path
from verification_component import render_art

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-1500:])
    return p.stdout

with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp);img=root/"review.png";out=root/"smoke.mp4"
    render_art(2.3).resize((1080,1920)).save(img)
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate","30","-i",str(img),
         "-f","lavfi","-i","sine=frequency=440:sample_rate=48000","-t","2",
         "-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p","-c:a","aac","-shortest",str(out)])
    p=json.loads(run(["ffprobe","-v","error","-show_entries",
       "stream=codec_name,width,height,r_frame_rate,sample_rate:format=duration","-of","json",str(out)]))
    assert any(s.get("codec_name")=="h264" and (s.get("width"),s.get("height"))==(1080,1920) and s.get("r_frame_rate")=="30/1" for s in p["streams"])
    assert any(s.get("codec_name")=="aac" for s in p["streams"])
    run(["ffmpeg","-hide_banner","-loglevel","error","-xerror","-i",str(out),"-f","null","-"])
    print("PASS: synthetic 2s 1080x1920 H264/AAC full decode")
