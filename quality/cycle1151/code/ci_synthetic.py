"""No user assets. Synthetic 9s H.264/AAC video exercises the scene03 proof reveal."""
import json, subprocess, tempfile
from pathlib import Path
from animated_proof_chart import run, PALETTES

with tempfile.TemporaryDirectory() as d:
    root=Path(d); src=root/'source.mp4'; out=root/'result.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','lavfi','-i','color=c=0x061c2a:s=1080x1920:r=30:d=9',
        '-f','lavfi','-i','sine=frequency=210:sample_rate=48000:duration=9',
        '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
        '-c:a','aac','-shortest',str(src)],check=True)
    report=run(src,out,preset='ultrafast')
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames',
        '-show_streams','-of','json',str(out)]))
    v=next(x for x in info['streams'] if x['codec_type']=='video')
    a=next(x for x in info['streams'] if x['codec_type']=='audio')
    assert (v['width'],v['height'],int(v['nb_read_frames']))==(1080,1920,270)
    assert a['codec_name']=='aac' and a['sample_rate']=='48000'
    assert report['overlay_frames']==79 and len(PALETTES)==10
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
    print('PASS: synthetic 270-frame 1080x1920 H264/AAC render/decode; 10 genre palettes')
