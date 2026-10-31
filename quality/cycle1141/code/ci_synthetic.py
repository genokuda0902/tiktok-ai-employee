"""Two-second synthetic-only CI; never uses or uploads private media."""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from caption_island import render,probe

def run(cmd):
    subprocess.run(cmd,check=True)

def audio_sha(path):
    raw=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error',
        '-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-'])
    return hashlib.sha256(raw).hexdigest()

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        stable=root/'stable.mp4'
        moving=root/'moving.mp4'
        output=root/'output.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-f','lavfi','-i','color=c=0x092334:s=1080x1920:r=30:d=2',
             '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
             '-vf','drawbox=x=0:y=1350:w=1080:h=570:color=black:t=fill,'
                   'drawbox=x=100:y=1470:w=700:h=140:color=0x77ffff:t=fill,'
                   'drawbox=x=150:y=200:w=400:h=400:color=0x336699:t=fill',
             '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
             '-c:a','aac','-shortest',str(stable)])
        run(['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-i',str(stable),'-vf','scale=1120:1992,crop=1080:1920:20:36',
             '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
             '-c:a','copy',str(moving)])
        render(moving,stable,output)
        run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
        info=probe(output)
        assert (info['width'],info['height'],info['fps'],info['frames'])==(1080,1920,'30/1',60),info
        assert audio_sha(moving)==audio_sha(output)
        print(json.dumps({'synthetic_ci':'PASS','frames':60,
                          'resolution':'1080x1920','aac_copied':True}))

if __name__=='__main__':
    main()
