"""Create 2-second 1080x1920 synthetic H264/AAC, deghost and decode."""
import sys,subprocess,tempfile
from pathlib import Path
import cv2,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from clean_cuts import render,probe
with tempfile.TemporaryDirectory() as d:
    p=Path(d);raw=p/'in.mp4';out=p/'out.mp4'
    proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24',
      '-s','1080x1920','-r','30','-i','pipe:0',
      '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
      '-map','0:v','-map','1:a','-c:v','libx264','-preset','ultrafast',
      '-crf','28','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-t','2',str(raw)],
      stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    for i in range(60):
        f=np.full((1920,1080,3),(25,25,40),dtype=np.uint8)
        cv2.putText(f,'SLIDE '+str(1+(i>=20)+(i>=40)),(120,480),
                    cv2.FONT_HERSHEY_SIMPLEX,4,(240,240,240),7)
        proc.stdin.write(f.tobytes())
    proc.stdin.close();err=proc.stderr.read();assert proc.wait()==0,err.decode()
    r=render(raw,out,(20,40),3,5)
    assert r['frames']==60 and r['replaced_frames']==14
    assert probe(out)
    for stream in ('v:0','a:0'):
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),
          '-map','0:'+stream,'-f','null','-'],check=True)
    print('PASS: 60 frames H264/AAC synthetic render and full decode')
