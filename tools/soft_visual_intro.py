import subprocess

def render(source, output, seconds=0.28):
    if not 0 < seconds <= 1:
        raise ValueError('seconds must be in (0,1]')
    subprocess.run(['ffmpeg','-y','-i',str(source),'-vf',f'fade=t=in:st=0:d={seconds},format=yuv420p','-c:v','libx264','-crf','18','-c:a','copy','-movflags','+faststart',str(output)],check=True)
