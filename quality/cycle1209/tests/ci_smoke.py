"""CI smoke: 2s synthetic 1080x1920 H264/AAC; no external assets."""
from pathlib import Path
import subprocess,tempfile,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_audio_cues import render,source_metadata,video_hash

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-1200:])

with tempfile.TemporaryDirectory() as t:
    src=Path(t)/'synthetic.mp4';out=Path(t)/'output.mp4'
    run(['ffmpeg','-v','error','-y','-f','lavfi','-i',
         'color=c=0x14232d:s=1080x1920:r=30:d=2',
         '-f','lavfi','-i','sine=frequency=320:sample_rate=48000:duration=2',
         '-c:v','libx264','-preset','ultrafast','-crf','32','-pix_fmt','yuv420p',
         '-c:a','aac','-ar','48000','-ac','1','-shortest',
         '-metadata:s:a:0','language=jpn',str(src)])
    result=render(src,out,starts=(0,30,45))
    assert result['frames']==60
    assert video_hash(src)==video_hash(out)
    assert source_metadata(out)[0]==60
    run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
    print('CI_SMOKE_PASS synthetic 60 frames, H264 copy, AAC decode')
