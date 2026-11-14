from pathlib import Path
import subprocess
from render import render
def test_review_is_silent_and_vertical(tmp_path):
    out=tmp_path/"review.mp4"
    render(out)
    assert out.stat().st_size>1000
    p=subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type,width,height","-of","csv=p=0",str(out)],capture_output=True,text=True,check=True)
    assert "1080,1920" in p.stdout
    assert "audio" not in p.stdout
    subprocess.run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"],check=True)
