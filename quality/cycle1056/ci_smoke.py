"""Offline synthetic video smoke; never uploads or claims full 23s review video."""
import json,subprocess,tempfile
from pathlib import Path
from proof_trace import render_frame
with tempfile.TemporaryDirectory() as td:
    root=Path(td)
    for i in range(15):render_frame(i).save(root/f'frame_{i:03d}.png')
    out=root/'synthetic.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
      '-f','lavfi','-i','color=c=black:s=1080x1920:r=30:d=0.5',
      '-framerate','30','-i',str(root/'frame_%03d.png'),
      '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=0.5',
      '-filter_complex','[0:v][1:v]overlay=0:0:shortest=1[v]',
      '-map','[v]','-map','2:a:0','-c:v','libx264','-preset','ultrafast',
      '-pix_fmt','yuv420p','-c:a','aac',str(out)],check=True)
    raw=subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(out)])
    streams=json.loads(raw)['streams']
    assert {s['codec_name'] for s in streams}=={'h264','aac'},streams
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    print('PASS synthetic H264/AAC full decode')
