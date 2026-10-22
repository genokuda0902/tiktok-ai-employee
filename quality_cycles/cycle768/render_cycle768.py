"""Render a full review MP4 by changing only scene 3 (4.03-5.90 seconds)."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
import cv2
from motion_path import MotionSpec,apply_motion,W,H,FPS

def run(args):
    p=subprocess.run([str(args[0]),'-nostdin',*map(str,args[1:])],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(f'{args[0]} failed: {p.stderr[-1600:]}')

def render(source:Path, output:Path, workdir:Path):
    source,output,workdir=map(Path,(source,output,workdir))
    output.parent.mkdir(parents=True,exist_ok=True)
    workdir.mkdir(parents=True,exist_ok=True)
    spec=MotionSpec()
    cap=cv2.VideoCapture(str(source))
    n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps=cap.get(cv2.CAP_PROP_FPS)
    size=(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if n!=429 or size!=(W,H) or abs(fps-FPS)>.01:raise ValueError((n,size,fps))
    cap.set(cv2.CAP_PROP_POS_FRAMES,spec.start_frame)
    for i in range(spec.start_frame,spec.end_frame):
        ok,frame=cap.read()
        if not ok:raise RuntimeError(f'missing frame {i}')
        cv2.imwrite(str(workdir/f'frame_{i:03d}.png'),apply_motion(frame,i,spec))
    cap.release()
    scene=workdir/'scene3.mp4';video=workdir/'video_only.mp4'
    run(['ffmpeg','-y','-loglevel','error','-framerate',FPS,'-start_number',spec.start_frame,
         '-i',workdir/'frame_%03d.png','-frames:v',spec.end_frame-spec.start_frame,
         '-c:v','libx264','-preset','ultrafast','-crf','18','-threads','4','-pix_fmt','yuv420p',scene])
    fc=(f'[0:v]trim=end_frame={spec.start_frame},setpts=PTS-STARTPTS[a];'
        f'[1:v]setpts=PTS-STARTPTS[b];'
        f'[0:v]trim=start_frame={spec.end_frame},setpts=PTS-STARTPTS[c];'
        '[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v]')
    run(['ffmpeg','-y','-loglevel','error','-filter_complex_threads','2',
         '-i',source,'-i',scene,'-filter_complex',fc,'-map','[v]','-an',
         '-c:v','libx264','-preset','ultrafast','-crf','21','-threads','4',
         '-r',FPS,'-frames:v',n,'-movflags','+faststart',video])
    run(['ffmpeg','-y','-loglevel','error','-i',video,'-i',source,'-map','0:v:0','-map','1:a:0',
         '-c','copy','-movflags','+faststart',output])
    return {'output':str(output),'frames':n,'changed_range':[spec.start_frame,spec.end_frame],
            'audio':'stream copied from cycle767','effect':'semantic signal travel→screen activation'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--workdir',required=True)
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output,a.workdir),ensure_ascii=False))
