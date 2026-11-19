"""Reusable gentle audio outro; preserves video frames."""
import json, subprocess
def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(path)]))
def render(source,target,fade_seconds=0.65):
    duration=float(probe(source)["format"]["duration"])
    if not 0 < fade_seconds < duration:
        raise ValueError("invalid fade duration")
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(source),"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f"afade=t=out:st={duration-fade_seconds:.3f}:d={fade_seconds:.3f}","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",str(target)],check=True)
    return probe(target)
