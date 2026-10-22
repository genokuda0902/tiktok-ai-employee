"""Reusable zero-cost slideshow overlay with exact inherited AAC stream copy."""
from pathlib import Path
import argparse, json, subprocess

def call(cmd):subprocess.run(cmd,check=True)
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height,avg_frame_rate','-of','json',str(path)]))['streams'][0]
def render(source,slides,output,windows):
    source=Path(source);output=Path(output);slides=[Path(p) for p in slides]
    if len(slides)!=len(windows) or not slides:raise ValueError('slide/window count mismatch')
    previous=-1
    for start,end in windows:
        if not (0<=start<end and start>=previous):raise ValueError('invalid or unsorted time windows')
        previous=end
    for slide in slides:
        if not slide.is_file():raise FileNotFoundError(slide)
    frames=int(probe(source)['nb_read_frames']);output.parent.mkdir(parents=True,exist_ok=True)
    filters=[];prev='0:v'
    for i,(start,end) in enumerate(windows):
        out=f'v{i}';filters.append(f"[{prev}][{i+1}:v]overlay=0:0:enable='gte(t,{start})*lt(t,{end})'[{out}]");prev=out
    filters.append(f'[{prev}]format=yuv420p[vout]')
    tmp=output.with_name('_video_only.mp4')
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source)]
    for s in slides:cmd+=['-loop','1','-i',str(s)]
    cmd+=['-filter_complex',';'.join(filters),'-map','[vout]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','30','-frames:v',str(frames),'-movflags','+faststart',str(tmp)]
    try:
        call(cmd)
        call(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(tmp),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)])
    finally:tmp.unlink(missing_ok=True)
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--slides',nargs='+',required=True);p.add_argument('--output',required=True);p.add_argument('--windows-json',required=True)
    a=p.parse_args();print(render(a.input,a.slides,a.output,json.loads(a.windows_json)))
