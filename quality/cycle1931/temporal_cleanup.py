"""Denoise image region without filtering lower subtitle area."""
import subprocess
FILTER = "[0:v]split=2[base][work];[work]crop=iw:1380:0:0,hqdn3d=1.2:1.2:2:2[clean];[base][clean]overlay=0:0:shortest=1,format=yuv420p[v]"
def render(source, target):
    subprocess.run(["ffmpeg","-y","-i",source,"-filter_complex",FILTER,"-map","[v]","-map","0:a:0","-c:v","libx264","-preset","ultrafast","-crf","20","-c:a","copy","-movflags","+faststart",target],check=True)
