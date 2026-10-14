"""Build cycle569 from the inherited cycle568 MP4 with identical Japanese AAC."""
from pathlib import Path
import argparse, subprocess, json
from render_scene import render_frame
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'assets/cycle568.mp4'
OUTPUT=ROOT/'output/cycle569_THREE_STAGE_CODE_JA_HUMAN_REVIEW.mp4'
START_FRAME=215
N=29
def build(source=SOURCE,output=OUTPUT):
    source,output=Path(source),Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    frames=output.parent/'frames';frames.mkdir(exist_ok=True)
    stages=[]
    for i in range(N):
        stages.append(render_frame(i,frames/f'frame{i:03d}.png'))
    (output.parent/'animation_stages.json').write_text(json.dumps(stages,ensure_ascii=False,indent=2))
    graph=(f'[1:v]format=rgba,setpts=PTS+{START_FRAME}/30/TB[p];'
           '[0:v][p]overlay=50:270:eof_action=pass:repeatlast=0:format=auto,format=yuv420p[v]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate','30','-start_number','0','-i',str(frames/'frame%03d.png'),
         '-filter_complex',graph,'-map','[v]','-map','0:a:0',
         '-c:v','libx264','-preset','ultrafast','-crf','19','-r','30','-pix_fmt','yuv420p',
         '-c:a','copy','-t','15.6','-movflags','+faststart',str(output)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-3000:])
    return output
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,default=SOURCE)
    ap.add_argument('--output',type=Path,default=OUTPUT)
    a=ap.parse_args();print(build(a.source,a.output))
