"""Offline synthetic-only CI smoke; never uploads real media."""
import sys, tempfile, subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from hook_attention import render

def probe_frames(path):
    s=subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','default=noprint_wrappers=1:nokey=1',str(path)],text=True).strip()
    return int(s)

with tempfile.TemporaryDirectory() as d:
    d=Path(d); source=d/'synthetic.mp4';output=d/'output.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x0A1B2A:s=1080x1920:r=30:d=2',
      '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
      '-c:v','libx264','-preset','ultrafast','-crf','32','-pix_fmt','yuv420p',
      '-c:a','aac','-ar','48000','-metadata:s:a:0','language=jpn',str(source)],check=True)
    render(source,output,d/'overlays')
    assert probe_frames(source)==probe_frames(output)==60
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
    print('CI synthetic video 2s 60/60 frames, full decode PASS')
