"""Synthetic free CI smoke: two seconds of H264/AAC and full output decode."""
import sys
import tempfile
from pathlib import Path
import subprocess
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from audio_reactive_meter import render

with tempfile.TemporaryDirectory() as tmp:
    d=Path(tmp); src=d/'synthetic.mp4'; out=d/'reactive.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','lavfi','-i','color=c=0x101827:s=1080x1920:r=30:d=2',
        '-f','lavfi','-i','sine=frequency=300:sample_rate=48000:duration=2',
        '-c:v','libx264','-preset','ultrafast','-crf','30',
        '-c:a','aac','-b:a','96k','-frames:v','60',str(src)],check=True)
    report=render(src,out,d/'temp','ai',d/'qa.json')
    assert report['frames']==60 and report['aac_bitstream_identical']
    assert report['full_decode']=='PASS' and out.stat().st_size>20000
    print('PASS synthetic 1080x1920 2-second full decode; 60 frames; AAC identical')
