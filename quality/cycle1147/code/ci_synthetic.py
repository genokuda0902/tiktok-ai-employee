"""CI uses synthetic audio/video only; private source and final MP4 never uploaded."""
import hashlib,subprocess,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from scene_cue_audio import render,sha256,probe
with tempfile.TemporaryDirectory() as d:
    src=Path(d)/'synthetic.mp4';out=Path(d)/'output.mp4';stem=Path(d)/'sfx.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',
        'testsrc2=size=1080x1920:rate=30:duration=2.5',
        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2.5',
        '-c:v','libx264','-preset','ultrafast','-crf','30',
        '-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
    r=render(src,out,stem,sha256(src),[.7,1.7])
    p=probe(out)
    v=next(x for x in p['streams'] if x['codec_type']=='video')
    a=next(x for x in p['streams'] if x['codec_type']=='audio')
    assert (v['width'],v['height'],v['codec_name'],a['codec_name'],a['sample_rate'])==(1080,1920,'h264','aac','48000')
    assert len(r['cue_placements'])==2
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
    def video_hash(path):
        b=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0',
          '-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','-'])
        return hashlib.sha256(b).hexdigest()
    assert video_hash(src)==video_hash(out),'Video was modified'
    print('PASS 75/75 frames synthetic full A/V, 2 original cues, H264 identical')
