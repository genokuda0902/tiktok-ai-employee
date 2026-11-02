"""Fully synthetic rights-safe 1080x1920 30fps AAC/8-chapter smoke."""
import subprocess,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from slide_detail import render
def run(a): subprocess.run(a,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
with tempfile.TemporaryDirectory() as td:
    p=Path(td)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi',
         '-i','testsrc2=size=1080x1920:rate=30:duration=2',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
         '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac',
         '-b:a','96k','-shortest',str(p/'raw.mp4')])
    meta=[';FFMETADATA1']
    for i in range(8):
        meta+=['[CHAPTER]','TIMEBASE=1/1000',f'START={i*250}',f'END={(i+1)*250}',f'title=Scene {i+1}']
    (p/'chapters.ffmeta').write_text('\n'.join(meta)+'\n')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p/'raw.mp4'),
         '-i',str(p/'chapters.ffmeta'),'-map','0','-map_chapters','1','-c','copy',str(p/'source.mp4')])
    q=render(p/'source.mp4',p/'out.mp4',genre='career')
    assert q['frames']==60 and q['aac_bitstream_identical'] and q['chapters']==8
    print('PASS synthetic 1080x1920 60 frames / 8 chapters / full A/V decode')
