"""cycle618: 10-genre review-only match loop; requires local approved baseline."""
from __future__ import annotations
import argparse, json, subprocess
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from PIL import Image

GENRES=('ai_work','miniature','before_after','science','life_hacks','finance','food','travel','history','education')

@dataclass(frozen=True)
class LoopSpec:
    genre:str='ai_work'
    frames:int=27
    fps:int=30
    width:int=1080
    height:int=1920
    publication_status:str='NOT_APPROVED'
    def validate(self):
        if self.genre not in GENRES:raise ValueError('unsupported genre')
        if not 12<=self.frames<=45:raise ValueError('transition duration invalid')
        if self.fps!=30 or (self.width,self.height)!=(1080,1920):raise ValueError('unsupported format')
        if self.publication_status!='NOT_APPROVED':raise ValueError('publication prohibited')

def ease(x:float)->float:
    if not 0<=x<=1:raise ValueError('progress invalid')
    return x*x*(3-2*x)

def blend_frame(src:np.ndarray,opening:np.ndarray,i:int,n:int)->np.ndarray:
    if src.shape!=opening.shape or src.dtype!=np.uint8 or opening.dtype!=np.uint8:
        raise ValueError('image format mismatch')
    if not 0<=i<n or n<2:raise ValueError('frame index invalid')
    if i==0:return src.copy()
    if i==n-1:return opening.copy()
    a=ease(i/(n-1))
    return np.clip(src.astype(np.float32)*(1-a)+opening.astype(np.float32)*a,0,255).astype(np.uint8)

def seam_difference(a:np.ndarray,b:np.ndarray)->float:
    return float(np.abs(a.astype(np.float32)-b.astype(np.float32)).mean())

def run(cmd):
    return subprocess.run(cmd,check=True,text=True,capture_output=True)

def probe(path:Path)->dict:
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]).stdout)

def render(baseline:Path,output:Path,work:Path,spec:LoopSpec=LoopSpec())->dict:
    spec.validate()
    info=probe(baseline)
    v=next((s for s in info['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in info['streams'] if s['codec_type']=='audio'),None)
    if not v or not a:raise ValueError('video and audio required')
    if (v['width'],v['height'])!=(1080,1920):raise ValueError('resolution mismatch')
    rate=v.get('r_frame_rate','0/1').split('/')
    if abs(float(rate[0])/float(rate[1])-30)>.01:raise ValueError('frame rate mismatch')
    total=int(v.get('nb_frames',0))
    if total<spec.frames+10:raise ValueError('too few frames')
    work.mkdir(parents=True,exist_ok=True)
    opening=work/'first.png'
    run(['ffmpeg','-y','-v','error','-i',str(baseline),'-frames:v','1','-vf','scale=540:960',str(opening)])
    tail_dir=work/'tail_input';tail_dir.mkdir(exist_ok=True)
    start=(total-spec.frames)/30
    run(['ffmpeg','-y','-v','error','-ss',f'{start:.6f}','-i',str(baseline),
         '-frames:v',str(spec.frames),'-vf','scale=540:960',str(tail_dir/'%03d.png')])
    tail_files=sorted(tail_dir.glob('*.png'))
    if len(tail_files)!=spec.frames:raise ValueError('tail decode incomplete')
    first=np.asarray(Image.open(opening).convert('RGB'))
    tail=[np.asarray(Image.open(p).convert('RGB')) for p in tail_files]
    original_seam=seam_difference(tail[-1],first)
    if original_seam<1:raise ValueError('already matched loop; do not repeat')
    for i,src in enumerate(tail):
        Image.fromarray(blend_frame(src,first,i,spec.frames)).save(work/f'{i:03d}.png')
    seg=work/'segment.mp4'
    run(['ffmpeg','-y','-v','error','-framerate','30','-i',str(work/'%03d.png'),
         '-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','ultrafast',
         '-crf','18','-pix_fmt','yuv420p','-an',str(seg)])
    head=total-spec.frames
    filt=f'[0:v]trim=end_frame={head},setpts=PTS-STARTPTS[h];[1:v]setpts=PTS-STARTPTS[t];[h][t]concat=n=2:v=1:a=0[v]'
    run(['ffmpeg','-y','-v','error','-i',str(baseline),'-i',str(seg),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
         '-preset','ultrafast','-crf','18','-pix_fmt','yuv420p','-c:a','copy',
         '-movflags','+faststart',str(output)])
    result=probe(output)
    ov=next(s for s in result['streams'] if s['codec_type']=='video')
    if int(ov.get('nb_frames',-1))!=total:raise AssertionError('frame count changed')
    f=work/'out_first.png';l=work/'out_last.png'
    run(['ffmpeg','-y','-v','error','-i',str(output),'-frames:v','1','-vf','scale=540:960',str(f)])
    run(['ffmpeg','-y','-v','error','-sseof','-0.033333','-i',str(output),'-frames:v','1',
         '-vf','scale=540:960',str(l)])
    seam=seam_difference(np.asarray(Image.open(f).convert('RGB')),np.asarray(Image.open(l).convert('RGB')))
    if seam>=original_seam*.2:raise AssertionError('loop seam reduction under 80%')
    return {'frames':total,'transition_frames':spec.frames,'old_seam_mad':round(original_seam,3),
            'new_seam_mad':round(seam,3),'reduction_pct':round((1-seam/original_seam)*100,2),
            'genre':spec.genre,'review_only':True,'japanese_narration':'ABSENT'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(render(args.baseline,args.output,args.work),ensure_ascii=False,indent=2))
