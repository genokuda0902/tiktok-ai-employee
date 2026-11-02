"""Generate a tiny real 1080x1920 synthetic video and validate rendering."""
import json,subprocess,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from speech_cue import render
with tempfile.TemporaryDirectory() as d:
    source=Path(d)/'in.mp4';out=Path(d)/'out.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x101e30:s=1080x1920:r=30:d=1.1',
                    '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.1',
                    '-c:v','libx264','-preset','ultrafast','-crf','32','-c:a','aac','-shortest',str(source)],check=True)
    q=render(source,out)
    assert q['frames']==33 and q['aac_bitstream_identical']
    print(json.dumps({'smoke':'PASS','frames':q['frames'],'output_bytes':q['bytes']}))
