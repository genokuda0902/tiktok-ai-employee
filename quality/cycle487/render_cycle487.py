"""Review-only cycle487 progressive synthetic UI renderer. Reuses prior review audio, not new speech."""
import argparse, importlib.util, json, subprocess
from pathlib import Path
from PIL import ImageDraw
from motion import MotionShot, validate_motion, reveal_count, text_prefix
p=Path(__file__).resolve().parents[1]/'cycle486'/'render_cycle486.py'
spec=importlib.util.spec_from_file_location('prior',p)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
SHOTS=[('problem',1.5,3.5),('source',3.5,5.5),('typing',5.5,7.5),
('check',7.5,9.5),('output',9.5,12),('compare',14,17),('cta',17,20.166667)]
def stage(kind,i,n):
    im=prior.draw_scene(kind,[s[0] for s in SHOTS].index(kind)+1)
    d=ImageDraw.Draw(im);f=(i+1)/n
    d.rectangle((85,199,995,217),fill='#23455F')
    d.rectangle((85,199,85+int(910*f),217),fill='#4CE1FF')
    if kind=='typing':
        d.rounded_rectangle((138,805,945,950),radius=20,fill='white')
        prior.label(d,text_prefix('=SUM(B2:B5)',f)+'▌',175,825,63,'#173D59',True)
    if kind in ('source','check'):
        if kind=='check':prior.spreadsheet(d)
        y=788+min(3,int(f*4))*105
        d.rectangle((319,y,621,y+105),outline='#F3A32C',width=11)
    if kind=='output':
        d.rectangle((150,790,930,1345),fill='#12314C')
        for j,v in enumerate(prior.VALUES):
            x=205+j*188;bottom=1280;top=bottom-int(v*1.43*f)
            d.rounded_rectangle((x,top,x+110,bottom),radius=12,fill='#33B5F2' if j<3 else '#4EE7AE')
            prior.label(d,str(v),x+17,top-54,36,'white',True)
            prior.label(d,prior.MONTHS[j],x+18,bottom+25,36,'white')
    if kind=='compare':
        x=100 if i<n//2 else 560
        d.rounded_rectangle((x+9,635,x+411,1380),radius=26,outline='#FFE27D',width=13)
    if kind=='cta':
        d.rounded_rectangle((140,1360,940,1515),radius=32,outline='#FFE27D' if i%2 else '#4CE1FF',width=12)
    if kind=='problem':
        x=125+((i//2)%2)*435;y=720+((i//4)%2)*265
        d.rounded_rectangle((x+4,y+4,x+376,y+221),radius=26,outline='#FFE27D',width=10)
    return im
def run(cmd):
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL)
def render(source,out):
    out.parent.mkdir(parents=True,exist_ok=True)
    validate_motion([MotionShot('ai_productivity',a,b,reveal_count(b-a),caption=k) for k,a,b in SHOTS],20.166667)
    timeline=[('original',0,1.5,None)]+[('animated',a,b,k) for k,a,b in SHOTS[:5]]+[('original',12,14,None)]+[('animated',a,b,k) for k,a,b in SHOTS[5:]]
    clips=[]
    for j,(typ,a,b,k) in enumerate(timeline):
        clip=out.parent/f'clip_{j:02d}.mp4';frames=round((b-a)*30)
        if typ=='original':
            cmd=['ffmpeg','-y','-v','error','-ss',str(a),'-i',str(source),'-an']
        else:
            folder=out.parent/f'stages_{k}';folder.mkdir(exist_ok=True)
            for i in range(reveal_count(b-a)):stage(k,i,reveal_count(b-a)).save(folder/f'{i:03d}.jpg',quality=88)
            cmd=['ffmpeg','-y','-v','error','-framerate','4','-i',str(folder/'%03d.jpg'),'-vf','fps=30','-an']
        run(cmd+['-frames:v',str(frames),'-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',str(clip)])
        clips.append(clip)
    concat=out.parent/'concat.txt'
    concat.write_text(''.join("file '"+str(c.resolve())+"'\n" for c in clips))
    visual=out.parent/'visual_only.mp4'
    run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-c:v','copy',str(visual)])
    run(['ffmpeg','-y','-v','error','-i',str(visual),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-t','20.166667','-movflags','+faststart',str(out)])
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--source',type=Path,required=True);a.add_argument('--out',type=Path,required=True)
    x=a.parse_args();render(x.source,x.out)
