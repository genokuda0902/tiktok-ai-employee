"""Review-only MP4 renderer; preserves inherited AAC packets and burned captions.

python render.py INPUT.mp4 OUTPUT.mp4
Never uploads user media or posts to TikTok. Inherited asset rights remain unverified.
"""
import argparse,json,subprocess,tempfile
from pathlib import Path
from focus_guides import write_ass,validate

def probe(path):
    raw=subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'stream=codec_type,codec_name,width,height,avg_frame_rate,nb_frames,sample_rate:format=duration',
        '-of','json',str(path)])
    return json.loads(raw)

def render(source,destination):
    source,destination=Path(source).resolve(),Path(destination).resolve()
    if not source.is_file():raise FileNotFoundError(source)
    if source==destination:raise ValueError('do not overwrite input')
    meta=probe(source)
    v=next(s for s in meta['streams'] if s['codec_type']=='video')
    a=next(s for s in meta['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['avg_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('expected 1080x1920 30fps')
    if a['codec_name']!='aac' or a['sample_rate']!='48000':
        raise ValueError('expected inherited AAC 48kHz')
    validate(duration=float(meta['format']['duration']))
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle888_') as tmp:
        ass=write_ass(Path(tmp)/'focus.ass',duration=float(meta['format']['duration']))
        ass_filter=str(ass).replace(':','\\:')
        subprocess.run(['ffmpeg','-y','-v','error','-xerror','-i',str(source),
            '-vf','ass='+ass_filter,'-map','0:v:0','-map','0:a:0',
            '-frames:v',str(v['nb_frames']),'-c:v','libx264','-preset','veryfast',
            '-crf','19','-threads','2','-pix_fmt','yuv420p','-c:a','copy',
            '-movflags','+faststart',str(destination)],check=True)
    return destination

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('destination')
    a=p.parse_args()
    print(render(a.source,a.destination))
