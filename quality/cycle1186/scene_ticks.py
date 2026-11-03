"""Draw chapter ticks at observed visual cut times; review-only reusable helper."""
def marker_filter(cuts, duration, width=1080):
    if duration <= 0 or cuts != sorted(set(cuts)) or any(t <= 0 or t >= duration for t in cuts):
        raise ValueError("cuts must be unique, ordered, and inside duration")
    return ",".join(f"drawbox=x={round(width*t/duration)}:y=0:w=3:h=12:color=white@0.95:t=fill" for t in cuts)

def render(src, dst, cuts, duration):
    import subprocess
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",src,
      "-vf",marker_filter(cuts,duration),"-c:v","libx264","-preset","ultrafast",
      "-crf","21","-c:a","copy","-movflags","+faststart",dst],check=True)
