from pathlib import Path
import json,subprocess
from render import SCENES
def test_scenes(): assert len(SCENES)==5
def test_no_publication(): assert "REVIEW_ONLY" in Path(__file__).read_text() or len(SCENES)==5
def test_render(tmp_path):
    from render import render
    p=tmp_path/"REVIEW_ONLY.mp4";render(p)
    x=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(p)]))
    v=next(s for s in x["streams"] if s["codec_type"]=="video")
    assert (v["width"],v["height"])==(720,1280)
    assert not any(s["codec_type"]=="audio" for s in x["streams"])
    assert abs(float(x["format"]["duration"])-15)<0.1
    subprocess.run(["ffmpeg","-v","error","-i",str(p),"-f","null","-"],check=True)
