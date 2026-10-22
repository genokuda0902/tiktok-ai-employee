"""Render 14.314s review MP4; separate OpenCV and FFmpeg to avoid thread contention."""
from __future__ import annotations
import argparse,json,subprocess,sys
from pathlib import Path

START,END,FPS=121,177,30

def run(args):
    p=subprocess.run([str(args[0]),*map(str,args[1:])],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(f'{args[0]} failed: {p.stderr[-1600:].decode(errors="replace")}')

def render(source,output,workdir):
    source,output,workdir=map(Path,(source,output,workdir))
    output.parent.mkdir(parents=True,exist_ok=True);workdir.mkdir(parents=True,exist_ok=True)
    script=Path(__file__).resolve().parent/'render_frames.py'
    run([sys.executable,script,'--input',source,'--workdir',workdir])
    scene=workdir/'scene3.mp4';video=workdir/'video_only.mp4'
    run(['ffmpeg','-y','-nostdin','-loglevel','error','-framerate',FPS,'-start_number',START,
         '-i',workdir/'frame_%03d.png','-frames:v',END-START,
         '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',scene])
    fc=(f'[0:v]trim=end_frame={START},setpts=PTS-STARTPTS[a];'
        f'[1:v]setpts=PTS-STARTPTS[b];'
        f'[0:v]trim=start_frame={END},setpts=PTS-STARTPTS[c];'
        '[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]')
    run(['ffmpeg','-y','-nostdin','-loglevel','error','-filter_complex_threads','2',
         '-i',source,'-i',scene,'-filter_complex',fc,'-map','[v]','-an',
         '-c:v','libx264','-preset','ultrafast','-crf','21','-threads','4',
         '-r',FPS,'-frames:v',429,'-movflags','+faststart',video])
    run(['ffmpeg','-y','-nostdin','-loglevel','error','-i',video,'-i',source,'-map','0:v:0','-map','1:a:0',
         '-c','copy','-movflags','+faststart',output])
    return {'output':str(output),'frames':429,'changed_range':[START,END],
            'audio':'copied from cycle767','effect':'signal travel→screen activation'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--workdir',required=True)
    a=p.parse_args();print(json.dumps(render(a.input,a.output,a.workdir),ensure_ascii=False))
