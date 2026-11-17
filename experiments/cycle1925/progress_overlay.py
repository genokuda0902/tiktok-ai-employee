"""Genre-independent video progress indicator."""
import subprocess

def add_progress(source, output, duration, color="0x38d9cb"):
    if duration <= 0:
        raise ValueError("duration must be positive")
    overlay = f"[0:v][1:v]overlay=x='-W+W*min(t/{duration},1)':y=45:shortest=1:eval=frame,format=yuv420p[v]"
    cmd = ["ffmpeg","-y","-i",source,"-f","lavfi","-i",f"color=c={color}:s=1080x6:r=30","-filter_complex",overlay,"-map","[v]","-map","0:a:0","-c:v","libx264","-preset","veryfast","-crf","20","-c:a","copy","-movflags","+faststart","-t",str(duration),output]
    subprocess.run(cmd,check=True)
