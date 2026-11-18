"""Fade the final audio tail without re-encoding the H.264 video."""
import json, subprocess
def fade_tail(src, dst, fade=0.45):
    if not 0.1 <= fade <= 2.0: raise ValueError("fade out of range")
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",src]))
    duration=float(data["format"]["duration"])
    if duration <= fade: raise ValueError("input too short")
    subprocess.run(["ffmpeg","-y","-i",src,"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f"afade=t=out:st={duration-fade:.3f}:d={fade:.3f}","-c:a","aac","-b:a","160k","-ar","48000","-movflags","+faststart",dst],check=True)
