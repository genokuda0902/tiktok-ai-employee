"""Fail release validation for silent or missing Japanese narration."""
import json, subprocess, sys

def validate(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-of","json",path],capture_output=True,text=True,check=True)
    streams=json.loads(p.stdout)["streams"]
    video=next(s for s in streams if s["codec_type"]=="video")
    assert (video["width"],video["height"])==(1080,1920)
    assert video["codec_name"]=="h264"
    assert any(s["codec_type"]=="audio" for s in streams)
    # An AAC track alone is not proof of Japanese speech.
    r=subprocess.run(["ffmpeg","-v","info","-i",path,"-vn","-af","volumedetect","-f","null","-"],capture_output=True,text=True)
    assert r.returncode==0
    import re
    m=re.search(r"mean_volume:\\s*(-?[\\d.]+) dB",r.stderr)
    assert m and float(m.group(1)) > -45, "Silent audio: do not publish"
    # This cannot establish Japanese language or intelligibility: manual review remains mandatory.

if __name__=="__main__":validate(sys.argv[1])
