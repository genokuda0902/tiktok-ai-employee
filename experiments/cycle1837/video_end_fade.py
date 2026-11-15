import subprocess

def render(src, dst, duration, fade_seconds=0.35):
    if not 0 < fade_seconds < duration:
        raise ValueError('Invalid fade duration')
    start = max(0, duration - fade_seconds - 0.02)
    subprocess.run(['ffmpeg','-y','-i',src,'-vf',f'fade=t=out:st={start:.3f}:d={fade_seconds:.3f}','-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',dst],check=True)
