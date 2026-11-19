"""Reusable audio fade-out for image-slide videos."""
import json,subprocess

def render(src,dst,fade=.45):
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',src]))
    duration=float(p['format']['duration'])
    if not 0 < fade < duration: raise ValueError('invalid fade')
    subprocess.run(['ffmpeg','-y','-i',src,'-map','0:v:0','-map','0:a:0','-c:v','copy','-af',f'afade=t=out:st={duration-fade:.3f}:d={fade:.3f}','-c:a','aac','-b:a','192k','-ar','48000',dst],check=True)
