"""Reusable visual closing fade. Preserves audio without re-encoding."""
import json, subprocess

def render(src, dst, fade=0.18):
    if not 0.05 <= fade <= 0.5: raise ValueError("fade out of range")
    info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",src]))
    duration=float(info["format"]["duration"])
    if duration <= fade: raise ValueError("video too short")
    subprocess.run(["ffmpeg","-y","-i",src,"-vf",f"fade=t=out:st={duration-fade:.3f}:d={fade:.3f}","-map","0:v:0","-map","0:a:0","-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",dst],check=True)
