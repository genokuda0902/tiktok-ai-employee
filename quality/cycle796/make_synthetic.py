#!/usr/bin/env python3
"""CI-only synthetic colored image and tone. NOT a Japanese voice video."""
import json
import subprocess
import sys
from pathlib import Path
from audio_gap_bed import render

def main():
    out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
    src=out/'cycle796_SYNTHETIC_INPUT.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x122744:s=1080x1920:r=30:d=4',
        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=4',
        '-c:v','libx264','-preset','ultrafast','-crf','35','-pix_fmt','yuv420p',
        '-c:a','aac','-shortest',str(src)],check=True)
    base=Path(__file__).resolve().parent
    qa=render(base/'config.json',src,out/'cycle796_SYNTHETIC_REVIEW_ONLY.mp4',out/'qa.json',out/'bed.wav')
    assert qa['video_packet_sha256_unchanged']
    print(json.dumps({'CI_SYNTHETIC_ONLY':True,'output':str(out/'cycle796_SYNTHETIC_REVIEW_ONLY.mp4'),
                      'qa':str(out/'qa.json')}))
if __name__=='__main__':main()
