"""Cycle 2205: fail-closed MP4 publication quality gate (stdlib only)."""
import json
import subprocess
import sys

def inspect(path):
    p = subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],capture_output=True,text=True,check=True)
    data=json.loads(p.stdout)
    video=next((s for s in data["streams"] if s["codec_type"]=="video"),None)
    audio=[s for s in data["streams"] if s["codec_type"]=="audio"]
    decode=subprocess.run(["ffmpeg","-v","error","-i",path,"-f","null","-"],capture_output=True)
    result={"dimensions_ok": bool(video and video["width"]==1080 and video["height"]==1920),
            "decode_ok": decode.returncode==0,
            "audio_present": bool(audio),
            "duration_seconds": float(data["format"]["duration"])}
    result["publication_gate_pass"]=all(result[k] for k in ("dimensions_ok","decode_ok","audio_present"))
    return result

if __name__=="__main__":
    result=inspect(sys.argv[1])
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if result["publication_gate_pass"] else 2)
