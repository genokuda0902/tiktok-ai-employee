"""2-second synthetic CI only; full 22.5-second review MP4 is generated and QA-tested locally."""
import json,subprocess,tempfile
from pathlib import Path
from specificity_component import render_art
def run(args):
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-2000:])
    return p.stdout
with tempfile.TemporaryDirectory() as td:
    root=Path(td);image=root/'scene.png';mp4=root/'smoke.mp4'
    render_art(2.5).resize((1080,1920)).save(image)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','30','-i',str(image),'-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','2','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(mp4)])
    data=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate,sample_rate:format=duration','-of','json',str(mp4)]))
    assert any(s.get('codec_name')=='h264' and (s.get('width'),s.get('height'))==(1080,1920) and s.get('r_frame_rate')=='30/1' for s in data['streams'])
    assert any(s.get('codec_name')=='aac' for s in data['streams'])
    run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(mp4),'-f','null','-'])
    print('PASS synthetic 2s 1080x1920 H264/AAC decode')
