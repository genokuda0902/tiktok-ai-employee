"""Review-only reusable speech dynamics filter for 10 content genres."""
import argparse
import subprocess

def audio_filter(highpass_hz=85, threshold=0.12, ratio=2, peak_limit=0.89):
    if not 50 <= highpass_hz <= 150:
        raise ValueError('highpass out of range')
    if not 0 < threshold < 1 or not 1 <= ratio <= 4 or not 0 < peak_limit <= 1:
        raise ValueError('invalid dynamics setting')
    return (f'highpass=f={highpass_hz},'
            f'acompressor=threshold={threshold}:ratio={ratio}:attack=15:release=180:makeup=1.3,'
            f'alimiter=limit={peak_limit}')

def render(source, output):
    subprocess.run(['ffmpeg','-hide_banner','-y','-i',source,'-map','0:v:0','-map','0:a:0',
                    '-c:v','copy','-af',audio_filter(),'-c:a','aac','-b:a','160k',
                    '-movflags','+faststart',output],check=True)

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    a=p.parse_args();render(a.source,a.output)
