"""Cycle 541 smoke checks for existing MP4 files. Run locally: python qa_smoke.py file.mp4"""
import json
import subprocess
import sys

def probe(path):
    raw = subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",path],text=True)
    return json.loads(raw)["streams"]

def check(path):
    streams=probe(path)
    video=next(s for s in streams if s["codec_type"]=="video")
    audio=next(s for s in streams if s["codec_type"]=="audio")
    assert (video["width"],video["height"])==(1080,1920)
    assert video["codec_name"]=="h264"
    assert audio["codec_name"]=="aac"
    assert audio["sample_rate"]=="48000"
    assert video["r_frame_rate"]=="30/1"
    print("PASS: portrait H264 30fps and AAC 48kHz")

if __name__=="__main__":
    check(sys.argv[1])
