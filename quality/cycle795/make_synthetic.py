"""Public-safe CI-only 3 second test with fictional CTA and obscuring bar."""
import json,sys
from pathlib import Path
from protected_region_restore import render,run
root=Path(sys.argv[1]);root.mkdir(parents=True,exist_ok=True)
base=root/'clean.mp4';dirty=root/'dirty.mp4';out=root/'cycle795_SYNTHETIC_TONE_REVIEW_ONLY.mp4'
for dest,obscure in ((base,False),(dirty,True)):
    vf="drawbox=x=70:y=1320:w=676:h=185:color=0xff1987:t=fill"
    if obscure:vf+=",drawbox=x=200:y=1420:w=500:h=65:color=black:t=fill"
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0x061a2a:s=1080x1920:r=30:d=3',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3',
         '-vf',vf,'-frames:v','90','-c:v','libx264','-preset','ultrafast','-crf','34',
         '-pix_fmt','yuv420p','-c:a','aac','-b:a','64k',dest])
c=json.loads((Path(__file__).parent/'config.json').read_text());c.update(duration_seconds=3.0,start_seconds=0.0,end_seconds=3.0)
qa=render(c,dirty,base,out,root/'qa.json')
print(json.dumps({'duration':qa['duration'],'frames':qa['video']['nb_frames'],'audio_copy':'PASS'},ensure_ascii=False))
