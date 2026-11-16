"""Reusable subtitle contrast plate for 1080x1920 review videos."""
import subprocess
def render(source, output):
    vf = "drawbox=x=155:y=1360:w=760:h=110:color=black@0.22:t=fill"
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(source),"-vf",vf,"-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(output)],check=True)
