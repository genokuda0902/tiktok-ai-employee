"""Zero-cost end-to-end synthetic video+Japanese graphic+AAC smoke test."""
from pathlib import Path
import tempfile,subprocess,sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from make_slides import create
from render import render

def run(args):subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
with tempfile.TemporaryDirectory() as t:
    t=Path(t);src=t/'source.mp4';out=t/'result.mp4'
    run(['ffmpeg','-y','-v','error','-f','lavfi','-i','color=c=#123344:s=1080x1920:r=30:d=2','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)])
    slides=[]
    for i in (1,2,3):
        p=t/f's{i}.png';create(i).save(p);slides.append(p)
    render(src,slides,out,[(0.2,0.6),(0.6,1.1),(1.1,1.6)])
    run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'])
    j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,nb_frames','-of','json',str(out)]))
    assert j['streams'][0]['nb_frames']=='60',j
    assert (j['streams'][0]['width'],j['streams'][0]['height'])==(1080,1920)
    assert j['streams'][1]['codec_name']=='aac'
    print('PASS synthetic 1080x1920 MP4 + AAC full decode + 60 frames')
