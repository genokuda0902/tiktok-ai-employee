"""Cycle722: review-only kinetic reveal for any vertical 10-genre image-first video.
Reimplementation; not the original v33 renderer. No publication or auto-post.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import subprocess, json
ROOT=Path(__file__).resolve().parents[1]
PREVIOUS=Path("/mnt/data/cycle721/rendered/cycle721_NATIVE_CINEMATIC_NARRATED_REVIEW_ONLY.mp4")
OUTPUT=ROOT/"rendered/cycle722_KINETIC_REVEAL_NARRATED_REVIEW_ONLY.mp4"
GENRES=("ai_work","beauty","love_psychology","saving","sales_business",
        "career","health","science","travel_food","product_comparison")
SCENES={"hook":(0.0,3.2),"graph":(9.8,12.8)}
PUBLISH_ALLOWED=False

def overlays():
    assets=ROOT/"assets"; assets.mkdir(exist_ok=True)
    a=Image.new("RGBA",(842,258),(0,0,0,0))
    d=ImageDraw.Draw(a)
    d.rounded_rectangle((0,0,840,256),radius=25,fill=(209,244,233,255))
    d.rectangle((0,0,840,13),fill=(68,228,217,255))
    a.save(assets/"after_reveal.png")
    b=Image.new("RGBA",(860,405),(238,247,255,255))
    d=ImageDraw.Draw(b)
    d.rectangle((0,0,10,404),fill=(45,218,234,255))
    b.save(assets/"chart_reveal.png")
    return assets/"after_reveal.png",assets/"chart_reveal.png"

def filter_graph():
    return (
       "[0:v][1:v]overlay=x='123+920*min(1,max(0,(t-0.2)/1.55))':"
       "y=940:eval=frame:enable='between(t,0,2.0)'[v1];"
       "[v1][2:v]overlay="
       "x='135+900*min(1,max(0,(t-9.8)/2.6))':y=777:"
       "eval=frame:enable='between(t,9.8,12.75)',format=yuv420p[vout]"
    )

def render():
    if not PREVIOUS.is_file(): raise FileNotFoundError(PREVIOUS)
    a,b=overlays(); OUTPUT.parent.mkdir(exist_ok=True)
    silent=OUTPUT.with_name("cycle722_video_only.mp4")
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y",
         "-i",str(PREVIOUS),"-loop","1","-framerate","30","-i",str(a),
         "-loop","1","-framerate","30","-i",str(b),
         "-filter_complex",filter_graph(),"-map","[vout]",
         "-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",
         "-an","-frames:v","819",str(silent)]
    subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=250)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
        "-i",str(silent),"-i",str(PREVIOUS),"-map","0:v:0","-map","1:a:0",
        "-c","copy","-movflags","+faststart",str(OUTPUT)],
        check=True,capture_output=True,text=True,timeout=100)
    silent.unlink(missing_ok=True)
    return OUTPUT

def validate():
    meta=json.loads(subprocess.check_output(["ffprobe","-v","error","-count_frames",
        "-show_streams","-show_format","-of","json",str(OUTPUT)]))
    streams={s["codec_type"]:s for s in meta["streams"]}
    assert streams["video"]["codec_name"]=="h264"
    assert (streams["video"]["width"],streams["video"]["height"])==(1080,1920)
    assert streams["video"]["nb_read_frames"]=="819"
    assert streams["audio"]["codec_name"]=="aac"
    assert 27.25<float(meta["format"]["duration"])<27.5
    subprocess.run(["ffmpeg","-v","error","-i",str(OUTPUT),"-f","null","-"],
        check=True,capture_output=True,timeout=80)
    return meta

if __name__=="__main__":
    print(render())
    print("QA PASS",validate()["format"]["duration"])
