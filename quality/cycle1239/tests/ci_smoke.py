#!/usr/bin/env python3
"""Generate and decode a synthetic, rights-clean video with 8 chapters and AAC."""
import sys,subprocess,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import save_reuse_panel as s

def run(args):subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
with tempfile.TemporaryDirectory() as td:
    p=Path(td);meta=p/'chapters.txt'
    bounds=[0,200,400,600,800,1000,1200,3700,4000]
    meta.write_text(';FFMETADATA1\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={a}\nEND={b}\ntitle=scene{i+1}\n' for i,(a,b) in enumerate(zip(bounds,bounds[1:]))))
    src=p/'src.mp4';out=p/'out.mp4'
    run(['ffmpeg','-y','-v','error','-f','lavfi','-i','color=c=black:s=1080x1920:r=30:d=4',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=4',
         '-f','ffmetadata','-i',str(meta),'-map','0:v','-map','1:a','-map_metadata','2','-map_chapters','2',
         '-c:v','libx264','-preset','ultrafast','-crf','35','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','64k','-shortest',str(src)])
    qa=s.render(src,out,'travel')
    assert qa['frames']==120 and qa['chapters']==8 and qa['full_av_decode']=='PASS'
    print('synthetic 120-frame 8-chapter H264/AAC render/decode PASS')
