"""Fast frame-exact 1080x1920 scene replacement with source AAC bitstream copy."""
from pathlib import Path
import argparse, json, subprocess

def call(cmd):subprocess.run(cmd,check=True)
def probe(path):
    j=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height,avg_frame_rate','-of','json',str(path)]))
    return j['streams'][0]
def render(source,slides,output,windows,fps=30):
    source=Path(source);output=Path(output);slides=[Path(s) for s in slides]
    if len(slides)!=len(windows) or not slides:raise ValueError('slide/window count mismatch')
    if any(a<0 or a>=b for a,b in windows) or any(abs(windows[i][1]-windows[i+1][0])>0.0001 for i in range(len(windows)-1)):
        raise ValueError('windows must be contiguous, increasing, and nonnegative')
    info=probe(source);total=int(info['nb_read_frames'])
    if (info['width'],info['height'])!=(1080,1920) or info['avg_frame_rate']!='30/1':raise ValueError('source must be 1080x1920 at 30fps')
    bounds=[(round(s*fps),round(e*fps)) for s,e in windows]
    if bounds[0][0]<0 or bounds[-1][1]>total or any(a>=b for a,b in bounds) or any(bounds[i][1]!=bounds[i+1][0] for i in range(len(bounds)-1)):
        raise ValueError('windows must be contiguous, increasing, and in range')
    for slide in slides:
        if not slide.is_file():raise FileNotFoundError(slide)
    from PIL import Image
    for slide in slides:
        with Image.open(slide) as im:
            if im.size!=(1080,1920):raise ValueError('slide resolution invalid')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-filter_complex_threads','2','-i',str(source)]
    for slide,(a,b) in zip(slides,bounds):
        cmd+=['-loop','1','-framerate',str(fps),'-t',f'{(b-a)/fps:.9f}','-i',str(slide)]
    # Split source so the long unaffected ranges are decoded only once.
    flt=['[0:v]split=2[before][after]',f'[before]trim=end_frame={bounds[0][0]},setpts=PTS-STARTPTS[v0]']
    for i,(a,b) in enumerate(bounds,1):flt.append(f'[{i}:v]trim=end_frame={b-a},setpts=PTS-STARTPTS[v{i}]')
    n=len(bounds)+1
    flt.append(f'[after]trim=start_frame={bounds[-1][1]},setpts=PTS-STARTPTS[v{n}]')
    flt.append(''.join(f'[v{i}]' for i in range(n+1))+f'concat=n={n+1}:v=1:a=0,format=yuv420p[v]')
    tmp=output.with_name('_cycle764_video_only.mp4')
    cmd+=['-filter_complex',';'.join(flt),'-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p','-r',str(fps),'-frames:v',str(total),'-movflags','+faststart',str(tmp)]
    try:
        call(cmd)
        call(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(tmp),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)])
    finally:tmp.unlink(missing_ok=True)
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--slides',nargs='+',required=True);p.add_argument('--output',required=True);p.add_argument('--windows-json',required=True)
    a=p.parse_args();print(render(a.input,a.slides,a.output,json.loads(a.windows_json)))
