"""Review-only FFmpeg scene-boundary fades. Input must be approved for use."""
import argparse
import subprocess

def fade_filter(cuts, duration=0.12):
    if duration <= 0 or duration > 0.5:
        raise ValueError("duration must be within (0, 0.5]")
    cuts = sorted(float(t) for t in cuts)
    if any(t <= duration or (i and t - cuts[i-1] < 2*duration) for i,t in enumerate(cuts)):
        raise ValueError("cuts overlap or start too early")
    return ",".join(part for t in cuts for part in (
        f"fade=t=out:st={t-duration:.3f}:d={duration:.3f}",
        f"fade=t=in:st={t:.3f}:d={duration:.3f}"
    ))

def render(src, dst, cuts):
    filt = fade_filter(cuts)
    subprocess.run(["ffmpeg","-hide_banner","-y","-i",src,"-vf",filt,
                    "-c:v","libx264","-preset","medium","-crf","20",
                    "-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",dst],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("src");p.add_argument("dst");p.add_argument("--cuts",nargs="+",type=float,required=True)
    a=p.parse_args();render(a.src,a.dst,a.cuts)
