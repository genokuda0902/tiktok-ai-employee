"""Fail closed: audible energy is not evidence of Japanese narration."""
import json, re, subprocess, sys
def inspect(path):
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",path],capture_output=True,text=True)
    if p.returncode: return {"pass":False,"reason":"probe_failed"}
    info=json.loads(p.stdout)
    if not any(s.get("codec_type")=="audio" for s in info.get("streams",[])):return {"pass":False,"reason":"audio_missing"}
    duration=float(info.get("format",{}).get("duration",0))
    if duration<=0:return {"pass":False,"reason":"invalid_duration"}
    p=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",path,"-af","silencedetect=noise=-35dB:d=0.25","-f","null","-"],capture_output=True,text=True)
    if p.returncode:return {"pass":False,"reason":"decode_failed"}
    starts=[float(x) for x in re.findall(r"silence_start: ([\\d.]+)",p.stderr)]
    ends=[float(x) for x in re.findall(r"silence_end: ([\\d.]+)",p.stderr)]
    if len(starts)>len(ends):ends.append(duration)
    active=max(0,duration-sum(max(0,min(duration,e)-s) for s,e in zip(starts,ends)))
    return {"pass":False,"reason":"silent_audio" if active<0.75 else "japanese_narration_not_verified","active_seconds":round(active,3),"speech_verified":False}
if __name__=="__main__":print(json.dumps(inspect(sys.argv[1]),ensure_ascii=False,indent=2))
