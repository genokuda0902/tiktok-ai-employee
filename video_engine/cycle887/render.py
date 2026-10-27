"""Offline MP4 renderer. Run: python render.py input.mp4 output.mp4
Source narration and image reuse rights must be verified before publishing.
This program does not post, contact APIs or use credentials.
"""
import argparse,subprocess,tempfile,wave
from pathlib import Path
import numpy as np
from audio_reactive_header import audio_bands,bar_heights,draw_bars,HeaderGeometry

def run(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL)

def render(source,destination):
    source=Path(source);destination=Path(destination)
    if not source.is_file():raise FileNotFoundError(source)
    if not HeaderGeometry().safe():raise ValueError('unsafe overlay position')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle887_') as temp:
        temp=Path(temp)
        wav=temp/'mono.wav';overlay=temp/'wave.mkv'
        run(['ffmpeg','-y','-v','error','-i',str(source),'-vn','-ac','1','-ar','16000',str(wav)])
        with wave.open(str(wav)) as w:
            sr=w.getframerate()
            samples=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
        import json
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,avg_frame_rate','-of','json',str(source)]))
        video=info['streams'][0]
        if video['avg_frame_rate']!='30/1':raise ValueError('expected 30fps')
        frames=int(video['nb_frames'])
        heights=bar_heights(audio_bands(samples,sr,frames))
        p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','180x54','-r','30','-i','pipe:0','-an','-c:v','ffv1',str(overlay)],stdin=subprocess.PIPE)
        for h in heights:p.stdin.write(draw_bars(h).tobytes())
        p.stdin.close()
        if p.wait()!=0:raise RuntimeError('overlay encoding failed')
        graph='[1:v]format=rgba,colorkey=0x000000:0.10:0.0[w];[0:v][w]overlay=x=570:y=61:shortest=1:format=auto,format=yuv420p[v]'
        run(['ffmpeg','-y','-v','error','-i',str(source),'-i',str(overlay),'-filter_complex',graph,
             '-map','[v]','-map','0:a:0','-frames:v',str(frames),'-r','30','-c:v','libx264',
             '-preset','veryfast','-crf','19','-threads','2','-pix_fmt','yuv420p','-c:a','copy',
             '-movflags','+faststart',str(destination)])
    return destination

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('destination')
    a=p.parse_args();print(render(a.source,a.destination))
