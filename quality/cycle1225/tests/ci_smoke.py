"""Tiny synthetic AV + chapter smoke; no user assets or external calls."""
import sys, tempfile, subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from chapter_progress import render

def run(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

with tempfile.TemporaryDirectory() as td:
    p=Path(td)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi',
         '-i','color=c=0x071225:s=1080x1920:r=30:d=2','-f','lavfi',
         '-i','sine=frequency=350:sample_rate=48000:duration=2',
         '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','96k','-shortest',str(p/'raw.mp4')])
    lines=[';FFMETADATA1']
    for i in range(8):
        lines += ['[CHAPTER]','TIMEBASE=1/1000',f'START={250*i}',
                  f'END={250*(i+1)}',f'title=Scene {i+1}']
    (p/'chapters.ffmeta').write_text('\n'.join(lines)+'\n')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-i',str(p/'raw.mp4'),'-i',str(p/'chapters.ffmeta'),
         '-map','0','-map_chapters','1','-c','copy',str(p/'source.mp4')])
    qa=render(p/'source.mp4',p/'output.mp4',p/'work','business',p/'qa.json')
    assert qa['frames']==60 and qa['aac_bitstream_identical']
    print('synthetic 2s/60frame A/V + eight chapters full decode PASS')
