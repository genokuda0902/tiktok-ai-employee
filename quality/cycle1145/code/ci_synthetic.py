"""Synthetic-only CI: no private audio, frames, reference image or MP4 uploaded."""
import hashlib,subprocess,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from typography_cut import render,source_info,sha256
with tempfile.TemporaryDirectory() as d:
    source=Path(d)/'synthetic.mp4'
    output=Path(d)/'review.mp4'
    subprocess.run(['ffmpeg','-v','error','-y',
        '-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=2.5',
        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2.5',
        '-c:v','libx264','-preset','ultrafast','-crf','29',
        '-c:a','aac','-ar','48000','-shortest',str(source)],check=True)
    render(source,output,sha256(source))
    info=source_info(output)
    assert (info['width'],info['height'],info['frames'],info['video_codec'],info['audio_codec'])==(1080,1920,75,'h264','aac'),info
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True)
    def adts(p):
        b=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'])
        return hashlib.sha256(b).hexdigest()
    assert adts(source)==adts(output),'AAC changed'
    print('PASS synthetic 75/75 A/V decode; H264 1080x1920 30fps; AAC 48kHz byte-identical')
