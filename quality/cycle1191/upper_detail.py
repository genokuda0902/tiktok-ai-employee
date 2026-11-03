"""Review-only upper-image detail enhancer. Keep caption zone out of filter."""
import argparse
import subprocess

def filtergraph(width=1080, height=1920, caption_zone=570, amount=0.35):
    assert width > 0 and 0 < caption_zone < height
    assert 0 <= amount <= 1
    upper = height - caption_zone
    return (f'[0:v]split=2[base][work];[work]crop={width}:{upper}:0:0,'
            f'unsharp=5:5:{amount}:5:5:0[detail];'
            f'[base][detail]overlay=0:0:format=auto,format=yuv420p[v]')

def render(source, target):
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
           '-filter_complex',filtergraph(),'-map','[v]','-map','0:a:0',
           '-c:v','libx264','-preset','veryfast','-crf','21',
           '-c:a','copy','-movflags','+faststart',target]
    subprocess.run(cmd, check=True)

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source')
    p.add_argument('target')
    a=p.parse_args()
    render(a.source,a.target)
