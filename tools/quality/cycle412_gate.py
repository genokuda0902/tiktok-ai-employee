"""Cycle412 fail-closed gate: never equate an AAC track with Japanese speech."""
import json, subprocess, math, array, sys
def run(cmd):
    return subprocess.run(cmd, capture_output=True, check=True).stdout
def check(path):
    obj=json.loads(run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))
    v=next((s for s in obj["streams"] if s["codec_type"]=="video"),None)
    a=next((s for s in obj["streams"] if s["codec_type"]=="audio"),None)
    if not v or v["codec_name"]!="h264" or (v["width"],v["height"])!=(1080,1920):
        raise ValueError("H.264 1080x1920 required")
    if not a or a["codec_name"]!="aac" or int(a["sample_rate"])!=48000:
        raise ValueError("AAC 48kHz required")
    raw=run(["ffmpeg","-v","error","-i",str(path),"-vn","-ar","8000","-ac","1","-f","s16le","-"])
    pcm=array.array("h"); pcm.frombytes(raw)
    if sys.byteorder!="little": pcm.byteswap()
    rms=math.sqrt(sum(x*x for x in pcm)/max(len(pcm),1))/32768
    run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"])
    return {"duration":float(obj["format"]["duration"]),"rms":rms,
            "japanese_voice":"NOT_GENERATED" if rms<.003 else "HUMAN_LISTENING_REQUIRED",
            "decode":"PASS","publication":"NOT_APPROVED"}
if __name__=="__main__": print(json.dumps(check(sys.argv[1]),ensure_ascii=False,indent=2))
