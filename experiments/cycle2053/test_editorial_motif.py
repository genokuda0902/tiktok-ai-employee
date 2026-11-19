from pathlib import Path
import subprocess, json
def test_vertical_video_metadata(video_path):
    info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(video_path)]))
    v=next(s for s in info["streams"] if s["codec_type"]=="video")
    a=next(s for s in info["streams"] if s["codec_type"]=="audio")
    assert (v["width"],v["height"],v["codec_name"])==(1080,1920,"h264")
    assert a["codec_name"]=="aac" and a["sample_rate"]=="48000"
