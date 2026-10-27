"""Synthetic-only FFmpeg integration smoke; never reads the private Japanese video."""
import json, subprocess, tempfile
from pathlib import Path
from kinetic_wipe import make_mask, filtergraph

def run(cmd):
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,timeout=80)

with tempfile.TemporaryDirectory() as d:
    d=Path(d); src=d/'source.mp4'; mask=d/'mask.png'; out=d/'out.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=blue:s=360x640:r=30:d=3',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3',
         '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)])
    make_mask(mask,width=360,caption_top=400)
    graph,pad=filtergraph(cuts=(45,),frames=90,half=4,width=360,caption_top=400)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-loop','1','-framerate','30','-i',str(mask),
         '-filter_complex',graph,'-map',pad,'-map','0:a:0','-frames:v','90',
         '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','copy',str(out)])
    run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(out),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,nb_frames','-of','json',str(out)]))
    assert p['streams'][0]['nb_frames']=='90' and p['streams'][1]['codec_name']=='aac'
    print('SYNTHETIC_AV_SMOKE_PASS: 90 frames, H264/AAC full decode')
