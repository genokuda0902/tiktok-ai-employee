"""Cycle411 reusable Japanese narration gate (10 genres). Never approve silent/tone tracks."""
import json, math, subprocess, array, sys
from pathlib import Path

def check(path):
    path = str(path)
    probe = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],capture_output=True,text=True,check=True)
    obj = json.loads(probe.stdout)
    v = next((s for s in obj["streams"] if s["codec_type"]=="video"),None)
    a = next((s for s in obj["streams"] if s["codec_type"]=="audio"),None)
    if not v or v["codec_name"]!="h264" or (v["width"],v["height"])!=(1080,1920):
        raise ValueError("Video must be H.264 1080x1920")
    if not a or a["codec_name"]!="aac" or int(a["sample_rate"])!=48000:
        raise ValueError("Audio must be AAC 48kHz")
    p = subprocess.run(["ffmpeg","-v","error","-i",path,"-vn","-ac","1","-ar","8000","-f","s16le","-"],capture_output=True,check=True)
    data = array.array("h"); data.frombytes(p.stdout)
    if sys.byteorder!="little": data.byteswap()
    if not data: raise ValueError("Empty audio")
    rms = math.sqrt(sum(x*x for x in data)/len(data))/32768
    if rms < .003: raise ValueError("Silent or very quiet audio: rms="+str(rms))
    # Non-silent is necessary, not sufficient: human Japanese listening still required.
    return {"codec":"h264/aac","size":"1080x1920","sample_rate":48000,
            "duration":float(obj["format"]["duration"]),"rms":rms,
            "japanese_listening":"HUMAN_REVIEW_REQUIRED","publication":"NOT_APPROVED"}

if __name__=="__main__":
    print(json.dumps(check(sys.argv[1]),ensure_ascii=False,indent=2))
