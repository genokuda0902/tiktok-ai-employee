"""No private media: one-second synthetic video+audio smoke."""
import subprocess
import tempfile
from pathlib import Path
from task_cards import draw_frame

def main():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)
        draw_frame(40).save(p/'overlay.png')
        out=p/'synthetic.mp4'
        subprocess.run(['ffmpeg','-v','error','-y',
            '-f','lavfi','-i','color=c=#0a1b32:s=1080x1920:r=30:d=1',
            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1',
            '-loop','1','-i',str(p/'overlay.png'),
            '-filter_complex','[0:v][2:v]overlay=0:0:shortest=1[v]',
            '-map','[v]','-map','1:a','-t','1','-c:v','libx264',
            '-preset','ultrafast','-crf','29','-pix_fmt','yuv420p',
            '-c:a','aac',str(out)],check=True,timeout=90)
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),
                        '-f','null','-'],check=True,timeout=60)
        assert out.stat().st_size>10000
    print('SYNTHETIC_AV_PASS')
if __name__=='__main__':main()
