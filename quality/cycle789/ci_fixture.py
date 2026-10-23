#!/usr/bin/env python3
"""Free synthetic visual-motion CI smoke fixture; NOT Japanese narration or production video."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg

def generate(output):
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    w,h,fps=1080,1920,30
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','pipe:0',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3',
         '-map','0:v:0','-map','1:a:0','-t','3','-c:v','libx264','-preset','ultrafast','-crf','28',
         '-pix_fmt','yuv420p','-c:a','aac','-b:a','64k','-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for n in range(90):
            im=Image.new('RGB',(w,h),(9,27,47));d=ImageDraw.Draw(im)
            d.rounded_rectangle((95,350,985,1460),radius=55,fill=(21,58,78),outline=(54,207,209),width=7)
            d.text((170,470),'REVIEW ONLY - SYNTHETIC FIXTURE',font=ImageFont.load_default(),fill='white')
            d.rounded_rectangle((145+n*3,680,520+n*3,1150),radius=32,fill=(62,159,190))
            d.text((170,1540),'NOT JAPANESE SPEECH / NOT FULL VIDEO',font=ImageFont.load_default(),fill='white')
            p.stdin.write(im.tobytes())
        p.stdin.close();err=p.stderr.read().decode(errors='replace');ret=p.wait()
        if ret:raise RuntimeError('ffmpeg: '+err[-2000:])
    finally:
        if p.poll() is None:p.kill()
    if not output.exists() or output.stat().st_size<10000:raise RuntimeError('MP4 not produced')
    result={'type':'synthetic_3s_fixture','not_full_user_video':True,'not_japanese_speech':True,
            'publication_approved':False,'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    output.with_suffix('.json').write_text(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    a=ap.parse_args();print(json.dumps(generate(a.output)))
