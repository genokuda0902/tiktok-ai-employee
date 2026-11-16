"""Review-only upscale of an approved/local source; no new audio is fabricated."""
import argparse
import subprocess

def command(src, dst):
    return ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-vf',
            'scale=1080:1920:flags=lanczos,eq=contrast=1.06:saturation=1.08,unsharp=5:5:0.45:3:3:0.0',
            '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
            '-movflags','+faststart','-an',str(dst)]

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source'); p.add_argument('output')
    a=p.parse_args()
    subprocess.run(command(a.source,a.output),check=True)
