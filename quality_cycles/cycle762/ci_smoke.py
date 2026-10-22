"""Synthetic video+audio CI test; does not certify Japanese voice or final MP4."""
from pathlib import Path
import tempfile,subprocess,json
from PIL import Image,ImageDraw
from render import render

def run(*args):subprocess.run(list(args),check=True,stdout=subprocess.DEVNULL)
def check():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);src=d/'in.mp4';out=d/'out.mp4'
        for n in (1,2):
            im=Image.new('RGB',(1080,1920),(15*n,60,85))
            ImageDraw.Draw(im).rectangle((100,200,800,1000),fill=(60,120*n,140))
            im.save(d/f'{n}.png')
        run('ffmpeg','-y','-loglevel','error','-f','lavfi','-i','color=c=navy:s=1080x1920:r=30:d=2',
            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2','-c:v','libx264','-preset','ultrafast','-crf','30',
            '-c:a','aac','-shortest',str(src))
        render(src,[d/'1.png',d/'2.png'],out,[(0.3,0.9),(0.9,1.9)])
        meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(out)]))['streams']
        assert len(meta)==2 and meta[0]['width']==1080 and meta[0]['height']==1920
        assert meta[0]['codec_name']=='h264' and meta[1]['codec_name']=='aac'
        run('ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-')
        print('CI synthetic MP4 video+AAC decode PASS')
if __name__=='__main__':check()
