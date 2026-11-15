import subprocess,sys
from pathlib import Path

def render(source, target):
    filt='[0:v]split=2[base][sub];[sub]crop=iw:180:0:1330,eq=contrast=1.14:brightness=0.008[enh];[base][enh]overlay=0:1330:format=auto,format=yuv420p[v]'
    subprocess.run(['ffmpeg','-y','-i',str(source),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-c:a','copy','-movflags','+faststart',str(target)],check=True)
if __name__=='__main__':render(Path(sys.argv[1]),Path(sys.argv[2]))
