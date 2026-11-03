"""Rights-safe CI smoke: synthetic color + synthetic sine only, no private media."""
from pathlib import Path
import sys, subprocess, tempfile, hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from microtext_repair import render

def call(*cmd):
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def sha_aac(p, target):
    call('ffmpeg','-v','error','-y','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts',str(target))
    return hashlib.sha256(target.read_bytes()).hexdigest()

with tempfile.TemporaryDirectory() as d:
    root=Path(d);src=root/'synthetic.mp4';out=root/'render.mp4'
    call('ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x071c26:s=1080x1920:r=30:d=4.2',
        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=4.2',
        '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src))
    render(src,out,preset='ultrafast',crf=24)
    call('ffmpeg','-v','error','-xerror','-i',str(out),'-map','0:v:0','-f','null','-',
        '-map','0:a:0','-f','null','-')
    assert sha_aac(src,root/'a.aac')==sha_aac(out,root/'b.aac')
    import json
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,nb_frames','-of','json',str(out)]))
    v=next(s for s in info['streams'] if s['codec_name']=='h264')
    assert (v['width'],v['height'],int(v['nb_frames']))==(1080,1920,126),v
    print('PASS synthetic 126 frames, 1080x1920, full AV decode, bit-identical AAC')
