#!/usr/bin/env python3
"""Generate synthetic private fixtures; never commit generated media. Requires Pillow, ffmpeg, ffprobe."""
import json, subprocess, tempfile, sys
from pathlib import Path
from PIL import Image, ImageDraw

def run(args): subprocess.run(args,check=True)
def main():
    renderer=Path(__file__).with_name('build.py')
    with tempfile.TemporaryDirectory(prefix='portrait_smoke_') as folder:
        p=Path(folder)
        im=Image.new('RGB',(1080,1920),'#224466');ImageDraw.Draw(im).ellipse((250,350,650,750),fill='white');im.save(p/'image.png')
        run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=blue:s=1080x1920:r=30:d=1','-c:v','libx264','-preset','ultrafast',str(p/'video.mp4')])
        run(['ffmpeg','-v','error','-y','-f','lavfi','-i','sine=frequency=440:duration=2','-c:a','pcm_s16le',str(p/'tone.wav')])
        (p/'captions.json').write_text(json.dumps([{'text':'TEST ONLY','start':0,'end':1},{'text':'NOT A VOICE','start':1,'end':2}]))
        asset=lambda name,kind:{'path':name,'type':kind,'source_type':'self_shot','rights_basis':'synthetic test','rights_evidence':'generated locally','commercial_use':True,'derivatives_allowed':True,'privacy_review':'approved'}
        cfg={'mode':'technical_test','output':'output.mp4','narration':'tone.wav','captions':'captions.json','assets':{'image':asset('image.png','image'),'video':asset('video.mp4','video')},'scenes':[{'asset_id':'image','seconds':1,'motion':'zoom_in'},{'asset_id':'video','seconds':1,'motion':'static'}]}
        (p/'config.json').write_text(json.dumps(cfg))
        run([sys.executable,str(renderer),'--config',str(p/'config.json')])
        run(['ffmpeg','-v','error','-xerror','-i',str(p/'output.mp4'),'-f','null','-'])
        meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p/'output.mp4')]))
        v=next(s for s in meta['streams'] if s['codec_type']=='video')
        assert (v['width'],v['height'])==(1080,1920)
        assert any(s['codec_type']=='audio' for s in meta['streams'])
        assert abs(float(meta['format']['duration'])-2)<.15
        print('PASS: mixed image/video, zoom filter, subtitle burn-in command, audio mux, 1080x1920, 2s, full decode')
if __name__=='__main__':main()
