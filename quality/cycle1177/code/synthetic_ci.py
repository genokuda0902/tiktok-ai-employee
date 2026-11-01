#!/usr/bin/env python3
"""Rights-safe synthetic 4-second H264/AAC end-to-end and audio-copy check."""
import hashlib,math,subprocess,sys,tempfile,wave
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from speech_pause_cue import render,probe

def cmd(args):subprocess.run(args,check=True)
def aac_sha(path):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
                                  '-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])
    return hashlib.sha256(data).hexdigest()

with tempfile.TemporaryDirectory() as d:
    d=Path(d);wav=d/'tone.wav';src=d/'synthetic.mp4';dst=d/'cue.mp4'
    with wave.open(str(wav),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000)
        import array
        samples=array.array('h')
        for i in range(48000*4):
            t=i/48000
            amp=0 if 1.3<=t<=1.7 else .18
            samples.append(int(32767*amp*math.sin(2*math.pi*440*t)))
        f.writeframes(samples.tobytes())
    cmd(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y',
         '-f','lavfi','-i','color=c=0x071523:s=1080x1920:r=30:d=4',
         '-i',str(wav),'-c:v','libx264','-preset','ultrafast','-crf','28',
         '-c:a','aac','-b:a','96k','-shortest',str(src)])
    result=render(src,dst)
    meta=probe(dst)
    v=next(s for s in meta['streams'] if s['codec_type']=='video')
    a=next(s for s in meta['streams'] if s['codec_type']=='audio')
    assert (v['codec_name'],int(v['width']),int(v['height']),int(v['nb_frames']))==('h264',1080,1920,120)
    assert a['codec_name']=='aac' and len(result['cues'])==1
    assert aac_sha(src)==aac_sha(dst),'AAC bitstream modified'
    cmd(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'])
    print('SYNTHETIC_CI_PASS 120 frames 1080x1920 AAC unchanged full decode')
