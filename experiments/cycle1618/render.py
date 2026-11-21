"""Review-only upscale of cycle1617. Requires locally supplied prior MP4; no automatic publication."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'cycle1617_REVIEW_ONLY.mp4'
OUTPUT=ROOT/'cycle1618_REVIEW_ONLY.mp4'
def render(source=SOURCE,output=OUTPUT):
    if not source.is_file(): raise FileNotFoundError(f'Missing approved synthetic input: {source}')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(source),'-vf','scale=1080:1920:flags=lanczos,eq=contrast=1.06:saturation=1.05,fade=t=in:st=0:d=0.25,fade=t=out:st=14.7:d=0.3','-r','24','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(output)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
    return output
if __name__=='__main__': print(render())
